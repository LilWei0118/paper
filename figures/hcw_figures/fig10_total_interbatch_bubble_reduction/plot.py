#!/usr/bin/env python3
"""Plot relative reduction in full-run inter-batch GPU compute gaps."""

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
SARATHI = Path("dataset_runs/sarathi_llama3_8b_3090_freq_bs64_128_256")
QWEN = Path("sglang_runs/sglang_qwen3_8b_3090_freq_bs64_128_256")
A100 = Path("sglang_runs/sglang_llama3_70b_a100_freq_bs128_256_512/stage7_auto")
DATASETS = [
    ("sharegpt", "ShareGPT", "#e66b64"),
    ("math", "MATH", "#64af85"),
    ("natural_questions", "Natural Questions", "#77b8de"),
]
MODELS = [
    ("sarathi", "Llama3-8B", (64, 128, 256), 2),
    ("qwen", "Qwen3-8B", (64, 128, 256), 2),
    ("a100", "Llama3-70B", (128, 256, 512), 1),
]
MODEL_COLORS = {"sarathi": "#77b8de", "qwen": "#e9a764", "a100": "#64af85"}


def read_csv(path):
    with path.open(newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sarathi_runs(data_root, dataset, bs, setting):
    path = data_root / SARATHI / "analysis/bubble_stage_runs.csv"
    selected = [
        row for row in read_csv(path)
        if row["dataset"] == dataset and int(row["bs"]) == bs
        and row["phase"] == "scan" and row["setting"] == setting
        and row["scope"] == "all_batches" and int(row["stage"]) in (1, 2)
    ]
    results = []
    for repeat in (1, 2):
        rows = [row for row in selected if int(row["repeat"]) == repeat]
        if sorted(int(row["stage"]) for row in rows) != [1, 2]:
            raise ValueError(f"Incomplete Sarathi stages: {dataset} BS{bs} {setting} rep{repeat}")
        results.append(dict(
            repeat=repeat,
            gap_s=sum(float(row["gap_us"]) for row in rows) / 1e6,
            gap_count=sum(int(row["gap_count"]) for row in rows),
            source=str(SARATHI / "analysis/bubble_stage_runs.csv"),
        ))
    return results


def sglang_stage(path, extension):
    """Include every measured batch mode, keeping the stage's execution order."""
    with path.open(newline="" if extension == "csv" else None) as file:
        rows = csv.DictReader(file) if extension == "csv" else (json.loads(line) for line in file)
        previous_end = None
        previous_id = None
        gap_total_ms = 0.0
        gap_count = 0
        for row in rows:
            if row["phase"] != "measurement":
                continue
            execution_id = int(row["execution_id"])
            start = float(row["compute_start_local_ms"])
            end = float(row["compute_end_local_ms"])
            if end <= start or (previous_id is not None and execution_id <= previous_id):
                raise ValueError(f"Invalid interval order: {path}")
            if previous_end is not None:
                gap = start - previous_end
                if gap < -0.02:
                    raise ValueError(f"Overlapping GPU intervals: {path}")
                gap_total_ms += max(0.0, gap)
                gap_count += 1
            previous_end = end
            previous_id = execution_id
    if gap_count == 0:
        raise ValueError(f"No measured inter-batch gaps: {path}")
    return gap_total_ms / 1000, gap_count


def sglang_runs(data_root, model, dataset, bs, setting, repeats):
    root = QWEN if model == "qwen" else A100
    folder = "math_train_use" if model == "a100" and dataset == "math" else dataset
    stages = range(1, 3) if model == "qwen" else range(1, 7)
    extension = "csv" if model == "qwen" else "jsonl"
    results = []
    for repeat in range(1, repeats + 1):
        run = root / folder / f"bs{bs}" / f"{setting}_rep{repeat}"
        totals = [sglang_stage(data_root / run / f"stage{stage}_batches.{extension}", extension)
                  for stage in stages]
        results.append(dict(
            repeat=repeat,
            gap_s=sum(total for total, _ in totals),
            gap_count=sum(count for _, count in totals),
            source=str(run),
        ))
    return results


def compute(data_root):
    choices = {
        (row["model"], row["dataset"], int(row["bs"])): row["selected_setting"]
        for row in read_csv(HERE / "selected_settings.csv")
    }
    assert len(choices) == 27
    summaries = []
    run_rows = []
    for model, _, sizes, repeats in MODELS:
        for dataset, _, _ in DATASETS:
            for bs in sizes:
                setting = choices[model, dataset, bs]
                getter = sarathi_runs if model == "sarathi" else sglang_runs
                if model == "sarathi":
                    auto = getter(data_root, dataset, bs, "auto")
                else:
                    auto = getter(data_root, model, dataset, bs, "auto", repeats)
                unavailable = model == "a100" and dataset == "sharegpt" and bs == 512
                if unavailable:
                    selected = []  # Selected Stage 3–6 JSONL data are unreadable.
                elif model == "sarathi":
                    selected = getter(data_root, dataset, bs, setting)
                else:
                    selected = getter(data_root, model, dataset, bs, setting, repeats)
                for label, records in (("auto", auto), (setting, selected)):
                    for record in records:
                        run_rows.append(dict(model=model, dataset=dataset, bs=bs,
                                             setting=label, **record))
                auto_mean = float(np.mean([record["gap_s"] for record in auto]))
                selected_mean = float(np.mean([record["gap_s"] for record in selected])) if selected else None
                summaries.append(dict(
                    model=model, dataset=dataset, bs=bs, selected_setting=setting,
                    auto_total_gap_s=auto_mean,
                    selected_total_gap_s="" if selected_mean is None else selected_mean,
                    bubble_reduction_pct="" if selected_mean is None else
                    100 * (auto_mean - selected_mean) / auto_mean,
                    repeats=repeats,
                    note="Selected Stage 3–6 JSONL files unreadable" if unavailable else "",
                ))
    return summaries, run_rows


def draw_model(ax, math_rows, model, label, sizes, low, high, show_ylabel):
    x = np.arange(len(sizes))
    for position, bs in zip(x, sizes):
        row = next(row for row in math_rows if row["model"] == model and int(row["bs"]) == bs)
        value = float(row["bubble_reduction_pct"])
        ax.bar(position, value, 0.62, color=MODEL_COLORS[model],
               edgecolor="black", linewidth=0.6)
        ax.text(position, value + 0.5, f"{value:.1f}",
                ha="center", va="bottom", fontsize=9)
    ax.set_title(label)
    ax.set_xticks(x, [str(bs) for bs in sizes])
    ax.tick_params(axis="both", which="both", direction="in")
    ax.set_xlabel("Batch size")
    if show_ylabel:
        ax.set_ylabel("Total bubble time reduction (%)")
    ax.set_ylim(low, high)
    ax.spines[["top", "right"]].set_visible(True)
    ax.axhline(0, color="black", lw=0.8)
    ax.grid(axis="y", ls="--", alpha=0.35)
    ax.set_axisbelow(True)


def save(fig, stems):
    for stem in stems:
        for extension in ("pdf", "png"):
            fig.savefig(stem.with_suffix(f".{extension}"), dpi=220)
    plt.close(fig)


def plot(summaries):
    math_rows = [row for row in summaries if row["dataset"] == "math"]
    assert len(math_rows) == 9 and all(row["bubble_reduction_pct"] for row in math_rows)
    values = [float(row["bubble_reduction_pct"]) for row in math_rows]
    low = min(0, 5 * np.floor((min(values) - 2) / 5))
    high = 5 * np.ceil((max(values) + 3) / 5)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11})
    fig, axes = plt.subplots(1, 3, figsize=(15.4, 4.5), sharey=True)
    for ax, (model, label, sizes, _) in zip(axes, MODELS):
        draw_model(ax, math_rows, model, label, sizes, low, high, ax is axes[0])
    fig.subplots_adjust(left=0.075, right=0.99, top=0.9, bottom=0.16, wspace=0.1)
    save(fig, (HERE / "Fig10_total_interbatch_bubble_reduction",
               HERE.parent / "Fig10_math_total_bubble_reduction_three_models_20261018"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("/home/hcw/LLM_pipeline_infer"))
    parser.add_argument("--refresh-data", action="store_true",
                        help="Recompute the all-dataset CSVs from local experimental runs")
    args = parser.parse_args()
    if args.refresh_data:
        summaries, runs = compute(args.data_root)
        write_csv(HERE / "bubble_reduction.csv", summaries)
        write_csv(HERE / "bubble_total_runs.csv", runs)
    else:
        summaries = read_csv(HERE / "bubble_reduction.csv")
    plot(summaries)
    print("Saved nine MATH configurations")


if __name__ == "__main__":
    main()
