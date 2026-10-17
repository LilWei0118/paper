#!/usr/bin/env python3
"""Rebuild the 27-panel Fig. 11 atlas with actual measured energy on blue axes."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent
ENERGY_COLOR = "#6baed6"
TIME_COLOR = "#ff766d"
DATASETS = (("sharegpt", "ShareGPT"), ("math", "MATH"),
            ("natural_questions", "Natural Questions"))
MODELS = (
    ("sarathi", "Llama3-8B · Sarathi · RTX 3090", (64, 128, 256)),
    ("qwen", "Qwen3-8B · SGLang · RTX 3090", (64, 128, 256)),
    ("a100", "Llama3-70B · SGLang · A100", (128, 256, 512)),
)
STEM = "Fig11_all_configs_atlas_output2_20261017"


def load():
    with (HERE / "values.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    for row in rows:
        row["bs"] = int(row["bs"])
        row["energy_kj"] = float(row["energy_kj"])
        row["inference_time_s"] = float(row["inference_time_s"])
        row["selected"] = row["selected"] == "True"
        row["provisional"] = row["provisional"] == "True"
    assert len(rows) == 279
    for model, _, sizes in MODELS:
        for dataset, _ in DATASETS:
            for bs in sizes:
                group = [row for row in rows if (row["model"], row["dataset"], row["bs"])
                         == (model, dataset, bs)]
                assert len(group) == (11 if model == "a100" else 10)
                assert sum(row["setting"] == "auto" for row in group) == 1
                assert sum(row["selected"] for row in group) == 1
                assert all(row["energy_kj"] > 0 and row["inference_time_s"] > 0 for row in group)
    return rows


def panel(ax, group, title):
    rows = sorted(group, key=lambda row: (row["setting"] != "auto",
                                          -int(row["frequency_mhz"] or 0)))
    x = np.arange(len(rows))
    energy = [row["energy_kj"] for row in rows]
    time = [row["inference_time_s"] for row in rows]
    chosen = next(i for i, row in enumerate(rows) if row["selected"])
    ax.axvspan(chosen - 0.38, chosen + 0.38, color="#e9f4ec", zorder=0)
    ax.plot(x, energy, "-o", color=ENERGY_COLOR, lw=1.6, ms=3.2)
    right = ax.twinx()
    right.plot(x, time, "-s", color=TIME_COLOR, lw=1.6, ms=3.0)
    ax.set_xticks(x, ["Auto" if row["setting"] == "auto" else row["frequency_mhz"]
                      for row in rows], rotation=50, ha="right")
    ax.set_xlim(-0.5, len(rows) - 0.5)
    ax.grid(axis="y", ls="--", alpha=0.35)
    ax.set_axisbelow(True)
    energy_range = max(energy) - min(energy)
    time_range = max(time) - min(time)
    ax.set_ylim(max(0, min(energy) - max(1, energy_range * 0.10)),
                max(energy) + max(1, energy_range * 0.16))
    right.set_ylim(min(time) - max(1, time_range * 0.10),
                   max(time) + max(1, time_range * 0.14))
    ax.set_title(title, fontsize=8.5)
    ax.tick_params(axis="x", labelsize=6.5)
    ax.tick_params(axis="y", labelsize=7.5, colors=ENERGY_COLOR)
    right.tick_params(axis="y", labelsize=7.5, colors=TIME_COLOR)
    ax.spines[["top"]].set_visible(False)
    right.spines[["top"]].set_visible(False)
    return right


def main():
    rows = load()
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, axes = plt.subplots(9, 3, figsize=(15.6, 27))
    for model_index, (model, name, sizes) in enumerate(MODELS):
        for dataset_index, (dataset, dataset_name) in enumerate(DATASETS):
            i = model_index * 3 + dataset_index
            for j, bs in enumerate(sizes):
                ax = axes[i, j]
                group = [row for row in rows if (row["model"], row["dataset"], row["bs"])
                         == (model, dataset, bs)]
                title = f"{name} · {dataset_name} · BS{bs}"
                if model == "a100" and dataset == "sharegpt" and bs == 512:
                    title += " *"
                right = panel(ax, group, title)
                if j == 0:
                    ax.set_ylabel("Energy (kJ)", color=ENERGY_COLOR, fontsize=8)
                if j == 2:
                    right.set_ylabel("Time (s)", color=TIME_COLOR, fontsize=8)
                if i == 8:
                    ax.set_xlabel("GPU clock cap (MHz)", fontsize=8)
    fig.suptitle("Fig. 11 · All 27 frequency-sweep configurations", y=0.998, fontsize=16)
    fig.text(0.5, 0.008,
             "Blue = measured total energy (kJ); red = inference time (s); "
             "pale green = lowest energy within 5% time increase. "
             "A100 output2. * ShareGPT BS512 provisional.",
             ha="center", fontsize=9)
    fig.subplots_adjust(left=0.075, right=0.94, top=0.975, bottom=0.035,
                        hspace=0.75, wspace=0.45)
    for extension in ("png", "pdf"):
        fig.savefig(OUTPUT / f"{STEM}.{extension}", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("Saved actual-energy atlas:", OUTPUT / STEM)


if __name__ == "__main__":
    main()
