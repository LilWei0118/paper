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
    ("sarathi", "Llama3-8B · Sarathi · RTX 3090", (64, 128, 256)),
    ("a100", "Llama3-70B · SGLang · A100", (128, 256, 512)),
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
        provisional = model == "a100" and bs == 512
        assert all((row["provisional"] == "True") == provisional for row in series)
        ax.plot([int(row["frequency_mhz"]) for row in series],
                [float(row["middle_stage_ms"]) for row in series],
                marker="o", color=color, lw=2, ms=4.5,
                label=f"BS{bs}" + (" (provisional)" if provisional else ""),
                ls="--" if provisional else "-")
    ax.set(title=title, xlabel="Configured GPU core frequency (MHz)",
           ylabel="Middle-stage decode time (ms)")
    ax.grid(ls="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9, loc="upper right")


def main():
    rows = load()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11})
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 6.8))
    for ax, (model, title, bss) in zip(axes, MODELS):
        panel(ax, model, title, bss, rows)
    fig.suptitle("ShareGPT · Fixed GPU frequency versus decode time", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    for stem in (OUTPUT, LEGACY_PREVIEW):
        fig.savefig(stem.with_suffix(".png"), dpi=220, bbox_inches="tight")
        fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {OUTPUT}.png and .pdf")


if __name__ == "__main__":
    main()
