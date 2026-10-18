#!/usr/bin/env python3
"""Rebuild the two-model ShareGPT Fig. 4 preview, x = 0–15,000 tokens."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent
COMBINED = "Fig4_auto_context_main_range_20261017"
MODELS = (
    ("SGLang / Qwen3-8B / 3090", "Qwen3-8B · SGLang · RTX 3090", (64, 128, 256), "qwen"),
    ("SGLang / Llama3-70B / A100", "Llama3-70B · SGLang · A100", (128, 256, 512), "llama70b"),
)
COLORS = ("#479ad1", "#f3af42", "#39b49b")


def load():
    with (HERE / "values.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 11512
    for row in rows:
        assert row["dataset"] == "sharegpt"
        row["bs"] = int(row["bs"])
        row["requests"] = int(row["requests"])
        row["x"] = int(row["x"])
        row["ms"] = float(row["ms"])
        assert 0 <= row["x"] <= 15000 and row["ms"] > 0
    return rows


def panel(ax, rows, key, title, sizes):
    selected = [row for row in rows if row["model"] == key]
    assert selected
    for color, bs in zip(COLORS, sizes):
        series = sorted((row for row in selected if row["bs"] == bs),
                        key=lambda row: row["x"])
        assert series
        requests = {row["requests"] for row in series}
        assert len(requests) == 1
        ax.scatter([row["x"] for row in series], [row["ms"] for row in series],
                   c=color, s=9, alpha=0.6, edgecolors="none",
                   label=f"BS{bs} / {requests.pop()} requests")
    ax.set(xlim=(0, 15000), ylim=(0, max(row["ms"] for row in selected) * 1.08),
           title=f"{title}\nShareGPT",
           xlabel="Sum of context lengths (tokens)",
           ylabel="Mean middle-stage CUDA time (ms)")
    ax.grid(ls="--", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)


def save(fig, path):
    for extension in ("png", "pdf"):
        fig.savefig(path.with_suffix(f".{extension}"), dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    rows = load()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11})
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.2))
    for ax, (key, title, sizes, _) in zip(axes, MODELS):
        panel(ax, rows, key, title, sizes)
    fig.suptitle("Auto · ShareGPT · rep1 · context length 0–15,000 tokens", fontsize=15)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    save(fig, OUTPUT / COMBINED)
    for key, title, sizes, stem in MODELS:
        fig, ax = plt.subplots(figsize=(7.2, 5.0))
        panel(ax, rows, key, title, sizes)
        fig.tight_layout()
        save(fig, HERE / f"Fig4_sharegpt_{stem}_x0_15000")
    print("Saved two-panel Fig. 4 and two model-specific views")


if __name__ == "__main__":
    main()
