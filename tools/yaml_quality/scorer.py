"""Rule-based quality scoring for extracted workflow YAML files."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from .constants import (
    EXTRACTED_REF_RE,
    GENERIC_TEXT_RE,
    GUIDE_DIMENSIONS,
    INPUT_REF_RE,
    STATE_REF_RE,
    STEP_ID_RE,
)
from .models import DimensionScore, WorkflowQuality


class ScoreBucket:
    """Collects pass/fail checks for one quality dimension."""

    def __init__(self, key: str, name: str) -> None:
        self.key = key
        self.name = name
        self.passed = 0
        self.total = 0
        self.findings: list[str] = []

    def add(self, passed: bool, message: str = "", weight: int = 1) -> None:
        """Add a weighted check result."""
        self.total += weight
        if passed:
            self.passed += weight
        elif message and message not in self.findings:
            self.findings.append(message)

    def to_score(self) -> DimensionScore:
        """Convert the bucket into a normalized dimension score."""
        score = 100.0 if self.total == 0 else self.passed / self.total * 100
        return DimensionScore(
            key=self.key,
            name=self.name,
            score=score,
            passed=self.passed,
            total=self.total,
            findings=self.findings[:8],
        )


def load_yaml(path: Path) -> Any:
    """Load YAML from disk."""
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalize_list(value: Any) -> list[Any]:
    """Normalize a YAML scalar or list into a list."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def as_mapping_by_name(items: Any) -> dict[str, dict[str, Any]]:
    """Return list-style schema objects keyed by their name."""
    result: dict[str, dict[str, Any]] = {}
    for item in normalize_list(items):
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            result[item["name"]] = item
    return result


def is_nonempty_text(value: Any) -> bool:
    """Return whether a YAML value is meaningful text."""
    return isinstance(value, str) and bool(value.strip()) and not GENERIC_TEXT_RE.search(value)


def step_ref(value: Any) -> str | None:
    """Extract a step id from a string or start_node mapping."""
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict) and isinstance(value.get("step_id"), str):
        return value["step_id"].strip() or None
    return None


def target_ref(value: Any) -> str | None:
    """Extract a transition target id."""
    return value.strip() if isinstance(value, str) and value.strip() else None


def score_workflows(workflows_root: Path) -> list[WorkflowQuality]:
    """Score every workflow directory under workflows_root."""
    results: list[WorkflowQuality] = []
    for workflow_path in sorted(workflows_root.glob("*/workflow.yaml")):
        steps_dir = workflow_path.parent / "steps"
        if steps_dir.is_dir():
            results.append(score_workflow(workflow_path, steps_dir))
    return results


def score_workflow(workflow_path: Path, steps_dir: Path) -> WorkflowQuality:
    """Score one workflow and its step directory."""
    workflow_name = workflow_path.parent.name
    buckets = {key: ScoreBucket(key, name) for key, name in GUIDE_DIMENSIONS}
    facts: dict[str, Any] = {}

    try:
        workflow = load_yaml(workflow_path)
        buckets["fallback"].add(isinstance(workflow, dict), "workflow.yaml 顶层不是字典", 5)
    except Exception as exc:  # noqa: BLE001 - report YAML errors as score findings
        workflow = {}
        buckets["fallback"].add(False, f"workflow.yaml 无法解析: {exc}", 5)

    if not isinstance(workflow, dict):
        workflow = {}

    step_ids = {
        item.strip()
        for item in normalize_list(workflow.get("steps"))
        if isinstance(item, str) and item.strip()
    }
    conclusions = workflow.get("conclusions") if isinstance(workflow.get("conclusions"), dict) else {}
    conclusion_ids = set(conclusions)

    step_docs = load_step_docs(steps_dir, buckets)
    actual_step_ids = set(step_docs)
    extraction_fields = build_extraction_field_index(step_docs)

    score_schema(workflow, buckets["schema"])
    score_topology(workflow, step_ids, actual_step_ids, conclusion_ids, buckets["topology"])
    score_steps(step_docs, buckets["step"])
    score_skills(step_docs, workflow_path.parent, buckets["skill"])
    score_conditions(workflow, step_docs, step_ids, conclusion_ids, extraction_fields, buckets["condition"])
    score_fallbacks(step_docs, conclusions, step_ids, conclusion_ids, buckets["fallback"])

    facts.update(
        {
            "workflow_step_count": len(step_ids),
            "step_file_count": len(actual_step_ids),
            "conclusion_count": len(conclusion_ids),
            "missing_step_files": sorted(step_ids - actual_step_ids),
            "orphan_step_files": sorted(actual_step_ids - step_ids),
        }
    )

    dimensions = [buckets[key].to_score() for key, _ in GUIDE_DIMENSIONS]
    overall = sum(item.score for item in dimensions) / len(dimensions)
    return WorkflowQuality(
        workflow=workflow_name,
        workflow_path=str(workflow_path),
        steps_dir=str(steps_dir),
        overall_score=overall,
        dimensions=dimensions,
        facts=facts,
    )


def load_step_docs(steps_dir: Path, buckets: dict[str, ScoreBucket]) -> dict[str, tuple[Path, dict[str, Any]]]:
    """Load step YAML documents keyed by declared or filename step id."""
    docs: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(steps_dir.glob("step_*.yaml")):
        try:
            raw = load_yaml(path)
        except Exception as exc:  # noqa: BLE001
            buckets["fallback"].add(False, f"{path.name} 无法解析: {exc}", 5)
            continue
        if not isinstance(raw, dict):
            buckets["step"].add(False, f"{path.name} 顶层不是字典", 3)
            continue
        step_id = raw.get("step_id") if isinstance(raw.get("step_id"), str) else path.stem
        docs[step_id] = (path, raw)
    return docs


def build_extraction_field_index(step_docs: dict[str, tuple[Path, dict[str, Any]]]) -> dict[str, dict[str, set[str]]]:
    """Build step -> result_key -> extracted field names."""
    index: dict[str, dict[str, set[str]]] = {}
    for step_id, (_, doc) in step_docs.items():
        per_result: dict[str, set[str]] = defaultdict(set)
        for skill in normalize_list(doc.get("skills")):
            if not isinstance(skill, dict):
                continue
            result_key = skill.get("result_key") if isinstance(skill.get("result_key"), str) else ""
            for item in normalize_list(skill.get("extraction_schema")):
                if isinstance(item, dict) and isinstance(item.get("name"), str):
                    per_result[result_key].add(normalize_field_name(item["name"]))
        index[step_id] = dict(per_result)
    return index


def normalize_field_name(name: str) -> str:
    """Normalize custom field names that accidentally include the custom marker."""
    return name.replace("[custom]", "").strip()


def score_schema(workflow: dict[str, Any], bucket: ScoreBucket) -> None:
    """Score extraction_guided.md Phase 1 requirements."""
    schema = as_mapping_by_name(workflow.get("input_schema"))
    facts = schema.get("facts", {})
    current_hop = schema.get("current_hop", {})
    bucket.add(bool(facts), "缺少 facts input_schema 对象", 3)
    bucket.add(bool(current_hop), "缺少 current_hop input_schema 对象", 3)

    props = as_mapping_by_name(current_hop.get("properties"))
    for field in ["hop_index", "current_device", "path_state"]:
        item = props.get(field)
        bucket.add(bool(item), f"current_hop 缺少必填基线字段 {field}", 2)
        if item:
            bucket.add(item.get("required") is True, f"{field} 未标记 required: true")
            bucket.add(is_nonempty_text(item.get("description")), f"{field} 缺少有效 description")

    all_props = list(as_mapping_by_name(facts.get("properties")).values()) + list(props.values())
    bucket.add(bool(all_props), "input_schema properties 为空", 2)
    for item in all_props:
        name = item.get("name", "<unknown>")
        bucket.add(isinstance(item.get("type"), str), f"{name} 缺少 type")
        bucket.add("required" in item, f"{name} 缺少 required 标记")
        bucket.add(is_nonempty_text(item.get("description")), f"{name} 缺少有效 description")


def score_topology(
    workflow: dict[str, Any],
    step_ids: set[str],
    actual_step_ids: set[str],
    conclusion_ids: set[str],
    bucket: ScoreBucket,
) -> None:
    """Score extraction guide Phase 2 skeleton requirements."""
    bucket.add(bool(step_ids), "workflow.steps 为空", 5)
    bucket.add(step_ids <= actual_step_ids, "workflow.steps 存在缺失的 step 文件", 5)
    bucket.add(actual_step_ids <= step_ids, "steps/ 存在未声明的 step 文件", 3)

    start_nodes = normalize_list(workflow.get("start_node"))
    bucket.add(bool(start_nodes), "start_node 为空", 4)
    for node in start_nodes:
        ref = step_ref(node)
        bucket.add(bool(ref and ref in step_ids), f"start_node 指向无效 step: {ref}", 2)
        if isinstance(node, dict):
            bucket.add(is_nonempty_text(node.get("description")), f"start_node {ref} 缺少 description")

    bucket.add(bool(conclusion_ids), "conclusions 为空", 4)
    duplicates = [item for item, count in Counter(normalize_list(workflow.get("steps"))).items() if count > 1]
    bucket.add(not duplicates, f"workflow.steps 存在重复声明: {', '.join(map(str, duplicates))}", 3)


def score_steps(step_docs: dict[str, tuple[Path, dict[str, Any]]], bucket: ScoreBucket) -> None:
    """Score per-step content completeness."""
    for step_id, (path, doc) in step_docs.items():
        bucket.add(path.stem == step_id, f"{path.name} 文件名与 step_id 不一致", 2)
        bucket.add(bool(STEP_ID_RE.match(step_id)), f"{step_id} 不符合 step_id 命名规范")
        bucket.add(is_nonempty_text(doc.get("name")), f"{step_id} 缺少 name")
        bucket.add(is_nonempty_text(doc.get("content")), f"{step_id} 缺少 content")
        bucket.add(doc.get("type") in {"diagnosis", "configuration"}, f"{step_id} type 无效")

        skills = [skill for skill in normalize_list(doc.get("skills")) if isinstance(skill, dict)]
        result_keys = [skill.get("result_key") for skill in skills if isinstance(skill.get("result_key"), str)]
        bucket.add(len(result_keys) == len(set(result_keys)), f"{step_id} 存在重复 result_key")

        for rule in normalize_list(doc.get("preconditions", {}).get("rules") if isinstance(doc.get("preconditions"), dict) else []):
            if isinstance(rule, dict):
                bucket.add(is_nonempty_text(rule.get("description")), f"{step_id} precondition 缺少 description")
                bucket.add(is_nonempty_text(rule.get("condition")), f"{step_id} precondition 缺少 condition")


def score_skills(step_docs: dict[str, tuple[Path, dict[str, Any]]], workflow_dir: Path, bucket: ScoreBucket) -> None:
    """Score skill and extraction_schema detail quality."""
    skill_asset_names = {path.stem for path in (workflow_dir / "user_skills").glob("**/*.yaml")}
    for step_id, (_, doc) in step_docs.items():
        skills = normalize_list(doc.get("skills"))
        if doc.get("type") == "diagnosis":
            bucket.add(bool(skills), f"{step_id} diagnosis step 缺少 skills", 3)
        for skill_index, skill in enumerate(skills):
            if not isinstance(skill, dict):
                bucket.add(False, f"{step_id} skills[{skill_index}] 不是字典", 3)
                continue
            skill_id = skill.get("skill_id")
            bucket.add(is_nonempty_text(skill_id), f"{step_id} skills[{skill_index}] 缺少 skill_id", 2)
            bucket.add(
                isinstance(skill_id, str) and skill_id.startswith("skill_"),
                f"{step_id} {skill_id} 不符合 skill_* 命名规范",
                2,
            )
            if isinstance(skill_id, str) and skill_id.startswith("skill_"):
                bucket.add(skill_id in skill_asset_names, f"{step_id} 引用的 {skill_id} 缺少 user_skills 定义")

            bucket.add(isinstance(skill.get("inputs") or {}, dict), f"{step_id} {skill_id} inputs 不是字典")
            bucket.add(is_nonempty_text(skill.get("selector")), f"{step_id} {skill_id} selector 为空或占位", 2)

            schema = normalize_list(skill.get("extraction_schema"))
            bucket.add(bool(schema) or doc.get("type") == "configuration", f"{step_id} {skill_id} extraction_schema 为空", 2)
            for item in schema:
                if not isinstance(item, dict):
                    bucket.add(False, f"{step_id} {skill_id} extraction_schema 条目不是字典")
                    continue
                field_name = item.get("name")
                bucket.add(is_nonempty_text(field_name), f"{step_id} {skill_id} 抽取字段缺少 name")
                bucket.add(isinstance(item.get("type"), str), f"{step_id} {field_name} 缺少 type")
                bucket.add(is_nonempty_text(item.get("description")), f"{step_id} {field_name} 缺少 description")
                if isinstance(field_name, str):
                    bucket.add(not field_name.startswith("[custom]"), f"{step_id} {field_name} 不应把 [custom] 放在 name")


def score_conditions(
    workflow: dict[str, Any],
    step_docs: dict[str, tuple[Path, dict[str, Any]]],
    step_ids: set[str],
    conclusion_ids: set[str],
    extraction_fields: dict[str, dict[str, set[str]]],
    bucket: ScoreBucket,
) -> None:
    """Score transition and precondition expressions."""
    schema = as_mapping_by_name(workflow.get("input_schema"))
    input_fields = {
        group: set(as_mapping_by_name(schema.get(group, {}).get("properties")).keys())
        for group in ["facts", "current_hop"]
    }
    valid_targets = step_ids | conclusion_ids

    for step_id, (_, doc) in step_docs.items():
        transitions = doc.get("transitions") if isinstance(doc.get("transitions"), dict) else {}
        rules = normalize_list(transitions.get("rules") if isinstance(transitions, dict) else [])
        for index, rule in enumerate(rules):
            if not isinstance(rule, dict):
                bucket.add(False, f"{step_id} transitions.rules[{index}] 不是字典", 2)
                continue
            condition = rule.get("condition")
            bucket.add(is_nonempty_text(rule.get("description")), f"{step_id} rule[{index}] 缺少 description")
            bucket.add(is_nonempty_text(condition), f"{step_id} rule[{index}] condition 为空", 2)
            if isinstance(condition, str):
                score_condition_refs(step_id, condition, extraction_fields, input_fields, step_ids, bucket)
                bucket.add(condition.strip().lower() != "true", f"{step_id} rule[{index}] 使用 True 兜底")
            target = target_ref(rule.get("next_node"))
            bucket.add(bool(target and target in valid_targets), f"{step_id} rule[{index}] next_node 无效: {target}", 2)

        preconditions = doc.get("preconditions") if isinstance(doc.get("preconditions"), dict) else {}
        for index, rule in enumerate(normalize_list(preconditions.get("rules"))):
            if isinstance(rule, dict) and isinstance(rule.get("condition"), str):
                score_condition_refs(step_id, rule["condition"], extraction_fields, input_fields, step_ids, bucket)


def score_condition_refs(
    step_id: str,
    condition: str,
    extraction_fields: dict[str, dict[str, set[str]]],
    input_fields: dict[str, set[str]],
    step_ids: set[str],
    bucket: ScoreBucket,
) -> None:
    """Validate refs used by a condition string."""
    for result_or_field, field in EXTRACTED_REF_RE.findall(condition):
        fields_by_result = extraction_fields.get(step_id, {})
        if field:
            valid = field in fields_by_result.get(result_or_field, set())
            bucket.add(valid, f"{step_id} condition 引用未声明字段 extracted.{result_or_field}.{field}", 2)
        else:
            valid = any(result_or_field in fields for fields in fields_by_result.values())
            bucket.add(valid, f"{step_id} condition 引用未声明字段 extracted.{result_or_field}", 2)

    for group, field in INPUT_REF_RE.findall(condition):
        bucket.add(field in input_fields.get(group, set()), f"{step_id} condition 引用未声明输入 input.{group}.{field}")

    for ref_step, _ in STATE_REF_RE.findall(condition):
        bucket.add(ref_step in step_ids, f"{step_id} condition 引用不存在的 state step: {ref_step}", 2)


def score_fallbacks(
    step_docs: dict[str, tuple[Path, dict[str, Any]]],
    conclusions: dict[str, Any],
    step_ids: set[str],
    conclusion_ids: set[str],
    bucket: ScoreBucket,
) -> None:
    """Score error handlers and conclusion completeness."""
    valid_targets = step_ids | conclusion_ids
    required_errors = {"handler_execution_failed", "cli_command_execution_failed", "parse_failure"}

    for step_id, (_, doc) in step_docs.items():
        transitions = doc.get("transitions") if isinstance(doc.get("transitions"), dict) else {}
        on_error = transitions.get("on_error") if isinstance(transitions.get("on_error"), dict) else {}
        bucket.add(required_errors <= set(on_error), f"{step_id} on_error 缺少标准错误兜底", 3)
        for key in required_errors & set(on_error):
            bucket.add(on_error[key] in valid_targets, f"{step_id} on_error.{key} 目标无效")
        bucket.add("default" not in transitions, f"{step_id} 存在已废弃的 transitions.default", 2)

    for conclusion_id, item in conclusions.items():
        if not isinstance(item, dict):
            bucket.add(False, f"{conclusion_id} 不是字典", 2)
            continue
        bucket.add(item.get("level") in {"info", "warning", "error", "critical"}, f"{conclusion_id} level 无效")
        bucket.add(is_nonempty_text(item.get("message")), f"{conclusion_id} 缺少 message")
        bucket.add(is_nonempty_text(item.get("suggestion")), f"{conclusion_id} 缺少 suggestion")
