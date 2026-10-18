#!/usr/bin/env python3
"""Rebuild the two-model Fig. 3 preview from its frozen Auto summaries."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent
STEM = "Fig3_auto_stage_idle_sharegpt_bs256_20261017"
SERIES = (
    ("Other Stages", "other_ms", "#087bb1", -1),
    ("Last Stage", "last_ms", "#efa500", 0),
    ("IDLE", "idle_ms", "#07a17e", 1),
)


def load():
    with (HERE / "values.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 2
    assert [row["model"].split("\n")[0] for row in rows] == ["Qwen3-8B", "Llama3-70B"]
    assert all(row["dataset"] == "ShareGPT" and row["bs"] == "256" for row in rows)
    for row in rows:
        for key in ("other_ms", "last_ms", "idle_ms"):
            row[key] = float(row[key])
            assert row[key] > 0
    return rows


def main():
    rows = load()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                         "axes.labelsize": 14, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    x = np.arange(len(rows))
    width = 0.25
    for label, key, color, position in SERIES:
        bars = ax.bar(x + position * width, [row[key] for row in rows], width,
                      label=label, color=color, edgecolor="black", linewidth=0.7)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height / 2,
                    f"{height:.1f}", ha="center", va="center", color="white",
                    fontweight="bold", fontsize=12)
    ax.set_xticks(x, [row["model"].split("\n")[0] for row in rows])
    ax.tick_params(axis="x", which="both", bottom=False, top=False)
    ax.tick_params(axis="y", which="both", direction="in")
    ax.set_ylabel("Time (ms)")
    ax.set_xlabel("Model")
    ax.set_ylim(0, max(row[key] for row in rows for _, key, _, _ in SERIES) * 1.2)
    ax.yaxis.grid(True, ls="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.13), frameon=False)
    fig.tight_layout()
    for extension in ("pdf", "png"):
        fig.savefig(OUTPUT / f"{STEM}.{extension}", dpi=240, bbox_inches="tight")
    plt.close(fig)
    print("Saved", OUTPUT / STEM)


if __name__ == "__main__":
    main()
