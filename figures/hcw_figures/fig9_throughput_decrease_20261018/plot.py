#!/usr/bin/env python3
"""Rebuild Fig. 9 with throughput decrease aligned to inference-time change."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "Fig9_energy_performance_three_models_output2_20261017"
DATASETS = (("sharegpt", "ShareGPT"), ("math", "MATH"),
            ("natural_questions", "Natural Questions"))
MODELS = (("sarathi", "Llama3-8B · Sarathi", (64, 128, 256)),
          ("qwen", "Qwen3-8B · SGLang", (64, 128, 256)),
          ("a100", "Llama3-70B · SGLang · A100", (128, 256, 512)))
METRICS = (("energy_efficiency_improvement_pct", "Energy efficiency gain", "#82c7e5"),
           ("inference_time_change_pct", "Inference time change", "#f0a526"),
           ("throughput_decrease_pct", "Throughput decrease", "#60b793"))


def load():
    with (HERE / "selected_settings.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 27
    assert len({(row["model"], row["dataset"], row["bs"]) for row in rows}) == 27
    for row in rows:
        row["throughput_decrease_pct"] = -float(row["throughput_change_pct"])
        assert float(row["inference_time_change_pct"]) * row["throughput_decrease_pct"] >= -1e-8
    return rows


def main():
    rows = load()
    lookup = {(row["model"], row["dataset"], int(row["bs"])): row for row in rows}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11})
    fig, axes = plt.subplots(3, 3, figsize=(16.8, 10.2), sharey=True)
    values = [float(row[key]) for row in rows for key, _, _ in METRICS]
    ylo = 5 * np.floor((min(values) - 2) / 5)
    yhi = 5 * np.ceil((max(values) + 4) / 5)
    for i, (model, title, sizes) in enumerate(MODELS):
        for j, (dataset, dataset_title) in enumerate(DATASETS):
            ax = axes[i, j]
            panel_rows = [lookup[(model, dataset, bs)] for bs in sizes]
            x = np.arange(len(sizes))
            width = 0.23
            for k, (key, label, color) in enumerate(METRICS):
                metric_values = [float(row[key]) for row in panel_rows]
                bars = ax.bar(x + (k - 1) * width, metric_values, width,
                              label=label, color=color, edgecolor="black", linewidth=0.5)
                for bar, value in zip(bars, metric_values):
                    ax.annotate(f"{value:.1f}",
                                (bar.get_x() + bar.get_width() / 2, value),
                                xytext=(0, 3 if value >= 0 else -3),
                                textcoords="offset points", ha="center",
                                va="bottom" if value >= 0 else "top", fontsize=7.3)
            ax.set_title(f"{dataset_title}\n{title}", fontsize=10.5)
            ax.set_xticks(x, [str(bs) for bs in sizes])
            ax.tick_params(axis="both", which="both", direction="in")
            ax.set_xlabel("Batch size")
            if j == 0:
                ax.set_ylabel("Change relative to Auto (%)")
            ax.set_ylim(ylo, yhi)
            ax.axhline(0, color="black", lw=0.8)
            ax.grid(axis="y", ls="--", alpha=0.35)
            ax.set_axisbelow(True)
            if model == "a100" and dataset == "sharegpt":
                ax.text(2, yhi - 2, "*", ha="center", fontsize=18)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=3, loc="upper center", frameon=False,
               bbox_to_anchor=(0.5, 0.995), fontsize=12)
    fig.text(0.5, 0.014,
             "Lowest energy with ≤5% inference-time increase. A100 uses output2 (Stage 7 Auto). "
             "* ShareGPT BS512 aggregate is provisional.",
             ha="center", fontsize=9)
    fig.subplots_adjust(top=0.91, bottom=0.095, left=0.065, right=0.99,
                        hspace=0.58, wspace=0.18)
    fig.savefig(OUTPUT.with_suffix(".png"), dpi=220)
    fig.savefig(OUTPUT.with_suffix(".pdf"))
    plt.close(fig)
    print(f"Saved {OUTPUT}.png and .pdf")


if __name__ == "__main__":
    main()
