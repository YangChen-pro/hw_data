"""Data models for YAML workflow quality scoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DimensionScore:
    """A normalized score for one quality dimension."""

    key: str
    name: str
    score: float
    passed: int
    total: int
    findings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WorkflowQuality:
    """Quality score and details for one workflow."""

    workflow: str
    workflow_path: str
    steps_dir: str
    overall_score: float
    dimensions: list[DimensionScore]
    facts: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "workflow": self.workflow,
            "workflow_path": self.workflow_path,
            "steps_dir": self.steps_dir,
            "overall_score": round(self.overall_score, 2),
            "dimensions": [
                {
                    "key": item.key,
                    "name": item.name,
                    "score": round(item.score, 2),
                    "passed": item.passed,
                    "total": item.total,
                    "findings": item.findings,
                }
                for item in self.dimensions
            ],
            "facts": self.facts,
        }
