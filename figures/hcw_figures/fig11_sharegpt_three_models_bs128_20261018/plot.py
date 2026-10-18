#!/usr/bin/env python3
"""Fig. 11: ShareGPT BS128 frequency sweeps for all three models."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "Fig11_sharegpt_three_models_bs128_output2_20261018"
PANELS = (
    ("sarathi", "(a) Llama3-8B · ShareGPT · BS128 · RTX 3090 · Sarathi"),
    ("qwen", "(b) Qwen3-8B · ShareGPT · BS128 · RTX 3090 · SGLang"),
    ("a100", "(c) Llama3-70B · ShareGPT · BS128 · A100 · SGLang"),
)
ENERGY = "#6baed6"
TIME = "#ff766d"


def load():
    with (HERE / "values.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 31
    for model, _ in PANELS:
        group = [row for row in rows if row["model"] == model]
        assert len(group) == (11 if model == "a100" else 10)
        assert sum(row["setting"] == "auto" for row in group) == 1
        assert all(row["dataset"] == "sharegpt" and row["bs"] == "128" for row in group)
        assert all(abs(float(row["energy_saved_vs_auto_kj"]) -
                       (float(row["auto_energy_kj"]) - float(row["energy_kj"]))) < 1e-8
                   for row in group)
    return rows


def draw(ax, group, title):
    rows = sorted((row for row in group if row["setting"] != "auto"),
                  key=lambda row: -int(row["frequency_mhz"]))
    x = np.arange(len(rows))
    energy = [float(row["energy_kj"]) for row in rows]
    time = [float(row["inference_time_s"]) for row in rows]
    energy_line, = ax.plot(x, energy,
                           "-o", color=ENERGY, lw=2, ms=4.8,
                           label="Total energy (kJ)")
    right = ax.twinx()
    time_line, = right.plot(x, time,
                            "-s", color=TIME, lw=2, ms=4.5,
                            label="Inference time (s)")
    ax.set_xticks(x, [row["frequency_mhz"] for row in rows])
    ax.set_xlim(-0.45, len(rows) - 0.55)
    energy_range = max(energy) - min(energy)
    time_range = max(time) - min(time)
    ax.set_ylim(max(0, min(energy) - max(1, energy_range * 0.25)),
                max(energy) + max(1, energy_range * 0.14))
    right.set_ylim(min(time) - max(1, time_range * 0.02),
                   max(time) + max(1, time_range * 0.30))
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("GPU SM clock cap (MHz)")
    ax.set_ylabel("Total energy (kJ)", color=ENERGY)
    right.set_ylabel("Inference time (s)", color=TIME)
    ax.tick_params(axis="y", colors=ENERGY)
    right.tick_params(axis="y", colors=TIME)
    ax.grid(axis="y", ls="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.spines[["top"]].set_visible(False)
    right.spines[["top"]].set_visible(False)
    return energy_line, time_line


def main():
    rows = load()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 10.3))
    for ax, (model, title) in zip(axes, PANELS):
        lines = draw(ax, [row for row in rows if row["model"] == model], title)
    fig.legend(lines, [line.get_label() for line in lines], loc="upper center",
               bbox_to_anchor=(0.5, 0.995), ncol=2, frameon=True)
    fig.subplots_adjust(left=0.11, right=0.89, top=0.93, bottom=0.065, hspace=0.53)
    fig.savefig(OUTPUT.with_suffix(".png"), dpi=220, bbox_inches="tight")
    fig.savefig(OUTPUT.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {len(rows) - 3} capped-frequency points in three panels")


if __name__ == "__main__":
    main()
