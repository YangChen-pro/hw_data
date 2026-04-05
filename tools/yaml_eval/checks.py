"""工作流 YAML 的结构检查逻辑。"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Any

from .models import (
    collect_references,
    is_placeholder_text,
    load_yaml,
    natural_step_key,
    normalize_list,
    read_text,
    LEGACY_STATE_REF_RE,
    Issue,
)
from .validators import find_line, validate_target


def evaluate_step(
    file_name: str,
    step_id: str,
    doc: dict[str, Any],
    raw_text: str,
    workflow_step_ids: set[str],
    conclusion_ids: set[str],
) -> list[Issue]:
    issues: list[Issue] = []
    declared_fields: set[str] = set()

    for skill_index, skill in enumerate(normalize_list(doc.get("skills"))):
        if not isinstance(skill, dict):
            issues.append(
                Issue(
                    file=file_name,
                    step_id=step_id,
                    severity="critical",
                    category="skill",
                    path=f"skills[{skill_index}]",
                    message="skill 结构不是字典",
                    recommendation="修正为包含 skill_id / inputs / selector / extraction_schema 的字典",
                )
            )
            continue

        extraction_schema = skill.get("extraction_schema") or []
        if not isinstance(extraction_schema, list):
            issues.append(
                Issue(
                    file=file_name,
                    step_id=step_id,
                    severity="critical",
                    category="extraction_schema",
                    path=f"skills[{skill_index}].extraction_schema",
                    message="extraction_schema 不是列表",
                    recommendation="改为列表结构；纯配置/纯操作步骤可使用 []",
                )
            )
            extraction_schema = []

        for item_index, item in enumerate(extraction_schema):
            if not isinstance(item, dict):
                issues.append(
                    Issue(
                        file=file_name,
                        step_id=step_id,
                        severity="critical",
                        category="extraction_schema",
                        path=f"skills[{skill_index}].extraction_schema[{item_index}]",
                        message="抽取字段条目不是字典",
                        recommendation="改为包含 name / type / description 的字典",
                    )
                )
                continue

            name = item.get("name")
            if isinstance(name, str) and name.strip():
                declared_fields.add(name.strip())
            else:
                issues.append(
                    Issue(
                        file=file_name,
                        step_id=step_id,
                        severity="critical",
                        category="extraction_schema",
                        path=f"skills[{skill_index}].extraction_schema[{item_index}].name",
                        message="抽取字段缺少 name",
                        recommendation="补充稳定的字段名",
                    )
                )

        inputs = skill.get("inputs") or {}
        if isinstance(inputs, dict):
            for input_key, input_value in inputs.items():
                if isinstance(input_value, str) and is_placeholder_text(input_value):
                    issues.append(
                        Issue(
                            file=file_name,
                            step_id=step_id,
                            severity="warning",
                            category="inputs",
                            path=f"skills[{skill_index}].inputs.{input_key}",
                            message=f"输入值看起来像占位符: {input_value}",
                            recommendation="替换为可由用户输入、前序结果或固定常量解析的真实值",
                        )
                    )
        else:
            issues.append(
                Issue(
                    file=file_name,
                    step_id=step_id,
                    severity="critical",
                    category="inputs",
                    path=f"skills[{skill_index}].inputs",
                    message="inputs 不是字典",
                    recommendation="改为 key/value 映射，常量可直接写，动态值需有明确来源",
                )
            )

    transitions = doc.get("transitions") or {}
    rules = normalize_list(transitions.get("rules"))
    for rule_index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            issues.append(
                Issue(
                    file=file_name,
                    step_id=step_id,
                    severity="critical",
                    category="transitions",
                    path=f"transitions.rules[{rule_index}]",
                    message="transition rule 不是字典",
                    recommendation="修正为包含 condition 和 next_node 的字典",
                )
            )
            continue

        condition = rule.get("condition")
        condition_path = f"transitions.rules[{rule_index}].condition"
        if condition is None or (isinstance(condition, str) and not condition.strip()):
            line = find_line(raw_text, r"^\s*condition:\s*(\"\"|''|\s*)$")
            issues.append(
                Issue(
                    file=file_name,
                    step_id=step_id,
                    severity="warning",
                    category="condition",
                    path=condition_path,
                    message="condition 为空",
                    recommendation="若分支依赖人工判断可保留；否则补充可规则化表达式",
                    line=line,
                )
            )
        elif isinstance(condition, str):
            line = find_line(raw_text, r"^\s*condition:\s*.*True.*$")
            if condition.strip().lower() == "true":
                issues.append(
                    Issue(
                        file=file_name,
                        step_id=step_id,
                        severity="warning",
                        category="condition",
                        path=condition_path,
                        message='condition 仅为 "True"',
                        recommendation="改为明确的判断条件，或注明这是人工兜底分支",
                        line=line,
                    )
                )

            if LEGACY_STATE_REF_RE.search(condition):
                issues.append(
                    Issue(
                        file=file_name,
                        step_id=step_id,
                        severity="warning",
                        category="condition",
                        path=condition_path,
                        message="condition 使用了 state.step_... 的旧式引用",
                        recommendation="如需和文档保持一致，可统一为 state.results.step_...；否则在文档中说明兼容旧格式",
                        line=line,
                    )
                )

            state_steps, extracted_fields, _ = collect_references(condition)
            for ref_step in sorted(state_steps):
                if ref_step not in workflow_step_ids:
                    issues.append(
                        Issue(
                            file=file_name,
                            step_id=step_id,
                            severity="critical",
                            category="condition",
                            path=condition_path,
                            message=f"引用了不存在的前序 step: {ref_step}",
                            recommendation="改为 workflow.yaml 中已声明的 step_id",
                            line=line,
                        )
                    )
            for field in sorted(extracted_fields):
                if field not in declared_fields:
                    issues.append(
                        Issue(
                            file=file_name,
                            step_id=step_id,
                            severity="critical",
                            category="extraction_schema",
                            path=condition_path,
                            message=f"condition 使用了未声明的 extracted 字段: {field}",
                            recommendation="把该字段补入 extraction_schema，或修改 condition",
                            line=line,
                        )
                    )

        next_node = rule.get("next_node")
        next_node_path = f"transitions.rules[{rule_index}].next_node"
        line = find_line(raw_text, rf"^\s*next_node:\s*{re.escape(str(next_node))}\s*$") if next_node is not None else None
        next_issues = validate_target(
            target=next_node,
            workflow_step_ids=workflow_step_ids,
            conclusion_ids=conclusion_ids,
            file_name=file_name,
            step_id=step_id,
            path=next_node_path,
        )
        for issue in next_issues:
            issues.append(replace(issue, line=line) if line is not None else issue)

    on_error = transitions.get("on_error") or {}
    if isinstance(on_error, dict):
        for key, target in on_error.items():
            issues.extend(
                validate_target(
                    target=target,
                    workflow_step_ids=workflow_step_ids,
                    conclusion_ids=conclusion_ids,
                    file_name=file_name,
                    step_id=step_id,
                    path=f"transitions.on_error.{key}",
                )
            )

    issues.extend(
        validate_target(
            target=transitions.get("default"),
            workflow_step_ids=workflow_step_ids,
            conclusion_ids=conclusion_ids,
            file_name=file_name,
            step_id=step_id,
            path="transitions.default",
        )
    )
    return issues


def evaluate_workflow(workflow_path: Path, steps_dir: Path) -> tuple[list[Issue], dict[str, Any]]:
    workflow = load_yaml(workflow_path)
    conclusions = workflow.get("conclusions") or {}
    conclusion_ids = set(conclusions.keys())
    workflow_step_ids = set(normalize_list(workflow.get("steps")))
    start_nodes = normalize_list(workflow.get("start_node"))

    issues: list[Issue] = []
    stats: dict[str, Any] = {
        "workflow_path": str(workflow_path),
        "steps_dir": str(steps_dir),
        "workflow_step_count": len(workflow_step_ids),
        "step_file_count": 0,
        "start_node_count": len(start_nodes),
        "blank_selector_count": 0,
        "blank_selector_examples": [],
        "files_with_issues": defaultdict(int),
        "issue_counter": Counter(),
    }

    for node in start_nodes:
        if node not in workflow_step_ids:
            issues.append(
                Issue(
                    file=workflow_path.name,
                    step_id="workflow",
                    severity="critical",
                    category="workflow",
                    path="start_node",
                    message=f"start_node 指向不存在的 step: {node}",
                    recommendation="改为 workflow.steps 中已声明的 step_id",
                )
            )

    actual_step_files = sorted(steps_dir.glob("step_*.yaml"), key=natural_step_key)
    stats["step_file_count"] = len(actual_step_files)
    actual_step_ids: set[str] = set()
    docs_by_step_id: dict[str, tuple[Path, dict[str, Any], str]] = {}

    for step_path in actual_step_files:
        raw_text = read_text(step_path)
        doc = load_yaml(step_path)
        step_id = str(doc.get("step_id") or step_path.stem)
        if step_id in docs_by_step_id:
            issues.append(
                Issue(
                    file=step_path.name,
                    step_id=step_id,
                    severity="critical",
                    category="workflow",
                    path="step_id",
                    message=f"发现重复的 step_id: {step_id}",
                    recommendation="保证每个 step_id 全局唯一",
                )
            )
        actual_step_ids.add(step_id)
        docs_by_step_id[step_id] = (step_path, doc, raw_text)

    for step_id in sorted(workflow_step_ids - actual_step_ids):
        issues.append(
            Issue(
                file="workflow.yaml",
                step_id="workflow",
                severity="critical",
                category="workflow",
                path="steps",
                message=f"workflow.yaml 声明了 step 但未找到文件: {step_id}",
                recommendation="补齐对应 step 文件或从 workflow.yaml 中移除该节点",
            )
        )

    for step_id in sorted(actual_step_ids - workflow_step_ids):
        issues.append(
            Issue(
                file=f"{step_id}.yaml",
                step_id=step_id,
                severity="warning",
                category="workflow",
                path="steps",
                message="发现 step 文件存在，但未在 workflow.yaml 的 steps 列表中声明",
                recommendation="若该文件属于正式流程，请补入 workflow.yaml；否则移除或归档",
            )
        )

    for step_id, (step_path, doc, raw_text) in docs_by_step_id.items():
        for skill_index, skill in enumerate(normalize_list(doc.get("skills"))):
            if isinstance(skill, dict):
                selector = skill.get("selector")
                if selector is None or (isinstance(selector, str) and not selector.strip()):
                    stats["blank_selector_count"] += 1
                    if len(stats["blank_selector_examples"]) < 8:
                        stats["blank_selector_examples"].append(f"{step_path.name}#skills[{skill_index}]")
        issues.extend(
            evaluate_step(
                file_name=step_path.name,
                step_id=step_id,
                doc=doc,
                raw_text=raw_text,
                workflow_step_ids=workflow_step_ids,
                conclusion_ids=conclusion_ids,
            )
        )

    for issue in issues:
        stats["files_with_issues"][issue.file] += 1
        stats["issue_counter"][issue.severity] += 1
        stats["issue_counter"][issue.category] += 1

    stats["files_with_issues"] = dict(sorted(stats["files_with_issues"].items()))
    stats["issue_counter"] = dict(stats["issue_counter"])
    return issues, stats
