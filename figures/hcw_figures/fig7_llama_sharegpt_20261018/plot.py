#!/usr/bin/env python3
"""Draw the two Llama ShareGPT panels selected for Fig. 7."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "Fig7_frequency_stage_time_llama_sharegpt_20261018"
LEGACY_PREVIEW = HERE.parent / "Fig7_frequency_stage_time_three_models_sharegpt_20261017"
MODELS = (
    ("sarathi", "Llama3-8B", (64, 128, 256)),
    ("a100", "Llama3-70B", (128, 256, 512)),
)
COLORS = ("#dec464", "#d76677", "#76c5e9")


def load():
    with (HERE / "sharegpt_frequency_means.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 57
    assert {row["model"] for row in rows} == {"sarathi", "a100"}
    assert all(row["dataset"] == "sharegpt" for row in rows)
    return rows


def panel(ax, model, title, bss, rows):
    for color, bs in zip(COLORS, bss):
        series = sorted((row for row in rows
                         if row["model"] == model and int(row["bs"]) == bs),
                        key=lambda row: int(row["frequency_mhz"]))
        assert len(series) == (10 if model == "a100" else 9)
        ax.plot([int(row["frequency_mhz"]) for row in series],
                [float(row["middle_stage_ms"]) for row in series],
                marker="o", color=color, lw=2, ms=4.5,
                label=f"BS{bs}", ls="-")
    ax.set(title=title, xlabel="Frequency (MHz)", ylabel="T(ms)")
    ax.tick_params(axis="both", which="both", direction="in")
    ax.grid(ls="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(True)
    ax.legend(fontsize=14, loc="upper right")


def main():
    rows = load()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16,
                         "axes.titlesize": 19, "axes.labelsize": 17,
                         "xtick.labelsize": 14, "ytick.labelsize": 14})
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 7.27))
    for ax, (model, title, bss) in zip(axes, MODELS):
        panel(ax, model, title, bss, rows)
    axes[0].set_xlabel("")
    fig.subplots_adjust(left=0.11, right=0.99, top=0.93, bottom=0.18,
                        hspace=0.30)
    for stem in (OUTPUT, LEGACY_PREVIEW):
        fig.savefig(stem.with_suffix(".png"), dpi=220)
        fig.savefig(stem.with_suffix(".pdf"))
    plt.close(fig)
    print(f"Saved {OUTPUT}.png and .pdf")


if __name__ == "__main__":
    main()
