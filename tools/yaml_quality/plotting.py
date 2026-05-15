"""Matplotlib chart rendering for YAML workflow quality scores."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

cache_root = Path(tempfile.gettempdir()) / "hw_data_matplotlib"
cache_root.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(cache_root))
os.environ.setdefault("XDG_CACHE_HOME", str(cache_root))

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np

from .models import WorkflowQuality


FONT_CANDIDATES = ["PingFang SC", "Heiti SC", "STHeiti", "Hiragino Sans GB", "Songti SC"]


def configure_chinese_font() -> str:
    """Configure Matplotlib to render Chinese labels and return the chosen font."""
    available = {font.name for font in font_manager.fontManager.ttflist}
    chosen = next((font for font in FONT_CANDIDATES if font in available), "")
    if chosen:
        plt.rcParams["font.sans-serif"] = [chosen] + plt.rcParams.get("font.sans-serif", [])
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 160
    plt.rcParams["savefig.dpi"] = 180
    return chosen


def write_charts(scores: list[WorkflowQuality], output_dir: Path) -> dict[str, str]:
    """Render all score charts into output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    chosen_font = configure_chinese_font()
    paths = {
        "overall_bar": output_dir / "overall_score_bar.png",
        "dimension_heatmap": output_dir / "dimension_score_heatmap.png",
        "radar": output_dir / "dimension_radar.png",
    }
    plot_overall_bar(scores, paths["overall_bar"], chosen_font)
    plot_dimension_heatmap(scores, paths["dimension_heatmap"], chosen_font)
    plot_dimension_radar(scores, paths["radar"], chosen_font)
    return {key: str(path) for key, path in paths.items()} | {"font": chosen_font or "Matplotlib default"}


def plot_overall_bar(scores: list[WorkflowQuality], output_path: Path, chosen_font: str) -> None:
    """Render a horizontal bar chart for overall scores."""
    ordered = sorted(scores, key=lambda item: item.overall_score)
    names = [item.workflow for item in ordered]
    values = [item.overall_score for item in ordered]
    colors = [score_color(value) for value in values]

    height = max(4.8, len(scores) * 0.7)
    fig, ax = plt.subplots(figsize=(10.5, height))
    bars = ax.barh(names, values, color=colors, edgecolor="#1f2937", linewidth=0.7)
    ax.set_xlim(0, 100)
    ax.set_xlabel("质量总分（0-100）")
    ax.set_title("YAML Workflow 质量总分", fontsize=16, pad=14)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.bar_label(bars, labels=[f"{value:.1f}" for value in values], padding=4)
    add_font_note(fig, chosen_font)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_dimension_heatmap(scores: list[WorkflowQuality], output_path: Path, chosen_font: str) -> None:
    """Render a heatmap of dimension scores per workflow."""
    names = [item.workflow for item in scores]
    dim_names = [item.name for item in scores[0].dimensions]
    matrix = np.array([[dim.score for dim in item.dimensions] for item in scores])

    fig_width = max(10, len(dim_names) * 1.7)
    fig_height = max(4.8, len(names) * 0.75)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    image = ax.imshow(matrix, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(np.arange(len(dim_names)), labels=dim_names, rotation=25, ha="right")
    ax.set_yticks(np.arange(len(names)), labels=names)
    ax.set_title("分维度质量得分热力图", fontsize=16, pad=14)

    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            color = "#111827" if matrix[row, col] > 55 else "#ffffff"
            ax.text(col, row, f"{matrix[row, col]:.0f}", ha="center", va="center", color=color, fontsize=9)

    cbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.025)
    cbar.set_label("得分")
    add_font_note(fig, chosen_font)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_dimension_radar(scores: list[WorkflowQuality], output_path: Path, chosen_font: str) -> None:
    """Render a radar chart comparing dimension scores."""
    dim_names = [item.name for item in scores[0].dimensions]
    angles = np.linspace(0, 2 * np.pi, len(dim_names), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(9, 8), subplot_kw={"projection": "polar"})
    palette = plt.cm.Set2(np.linspace(0, 1, len(scores)))
    for score, color in zip(scores, palette, strict=False):
        values = [dim.score for dim in score.dimensions]
        values += values[:1]
        ax.plot(angles, values, label=f"{score.workflow} ({score.overall_score:.1f})", linewidth=2, color=color)
        ax.fill(angles, values, color=color, alpha=0.08)

    ax.set_xticks(angles[:-1], labels=dim_names)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"])
    ax.set_title("分维度质量雷达图", fontsize=16, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.38, 1.12), frameon=False)
    add_font_note(fig, chosen_font)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def score_color(value: float) -> str:
    """Return a readable color by score band."""
    if value >= 85:
        return "#16a34a"
    if value >= 70:
        return "#65a30d"
    if value >= 55:
        return "#d97706"
    return "#dc2626"


def add_font_note(fig: plt.Figure, chosen_font: str) -> None:
    """Add a small footer showing the selected Chinese font."""
    note = f"中文字体：{chosen_font or '默认字体'}；专业术语保留英文"
    fig.text(0.01, 0.01, note, fontsize=8, color="#64748b")
