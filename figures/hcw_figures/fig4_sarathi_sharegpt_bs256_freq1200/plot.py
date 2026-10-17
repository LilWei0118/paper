#!/usr/bin/env python3
"""Plot Fig. 4 style context-length data for one Sarathi fixed-clock run."""

import argparse
import collections
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
RUN_RELATIVE = Path(
    "dataset_runs/sarathi_llama3_8b_3090_freq_bs64_128_256/"
    "sharegpt/bs256/scan/freq1200/rep1"
)
PREFIX = "Fig4_sarathi_sharegpt_bs256_freq1200_rep1"


def load_points(run):
    config = json.loads((run / "run.json").read_text())
    assert config["status"] == "completed"
    assert (config["dataset"], config["bs"], config["setting"], config["repeat"]) == (
        "sharegpt", 256, "freq1200", 1
    )
    events = json.loads((run / "inference/chrome_trace.json").read_text())
    stages = {
        stage: sorted(
            (
                event["args"] for event in events
                if event.get("tid") == stage
                and "cuda_stage_duration_us" in event.get("args", {})
            ),
            key=lambda row: row["batch_id"],
        )
        for stage in (1, 2)
    }
    assert [row["batch_id"] for row in stages[1]] == [
        row["batch_id"] for row in stages[2]
    ]
    outputs = {
        str(row["seq_id"]): row
        for row in json.loads((run / "request_outputs_summary.json").read_text())
    }
    decode = [
        row for row in stages[1]
        if row["num_batched_prompt_tokens"] == 0
        and row["num_batched_output_tokens"] > 0
    ]
    request_count = collections.Counter(row["batch_size"] for row in decode).most_common(1)[0][0]
    seen = collections.Counter()
    prompt = collections.Counter()
    points = []
    for first, second in zip(stages[1], stages[2]):
        assert first["request_ids"] == second["request_ids"]
        assert first["prompt_chunk_lens"] == second["prompt_chunk_lens"]
        request_ids = [str(value) for value in first["request_ids"]]
        pure_decode = first["num_batched_prompt_tokens"] == 0 and first["num_batched_output_tokens"] > 0
        context_lengths = []
        for request_id, chunk in zip(request_ids, first["prompt_chunk_lens"]):
            if chunk > 0:
                prompt[request_id] += chunk
            else:
                assert prompt[request_id] == outputs[request_id]["prompt_tokens"]
                context_lengths.append(outputs[request_id]["prompt_tokens"] + seen[request_id])
                seen[request_id] += 1
        if pure_decode and len(request_ids) == request_count:
            points.append({
                "batch_id": first["batch_id"],
                "requests": request_count,
                "context_tokens": sum(context_lengths),
                "middle_stage_ms": (
                    first["cuda_stage_duration_us"] + second["cuda_stage_duration_us"]
                ) / 2000,
            })
    assert all(
        seen[request_id] == output["output_tokens"]
        and prompt[request_id] == output["prompt_tokens"]
        for request_id, output in outputs.items()
    )
    return points, request_count


def write_csv(path, rows, fields):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def draw(rows, request_count, full_range):
    x = np.array([row["context_tokens"] for row in rows])
    y = np.array([row["middle_stage_ms"] for row in rows])
    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.scatter(x, y, c="#479ad1", s=12, alpha=0.65, edgecolors="none",
               label=f"BS256 / {request_count} requests")
    ax.set(
        xlim=(0, float(x.max()) * 1.03),
        xlabel="Sum of context lengths (tokens)",
        ylabel="Mean middle-stage CUDA time (ms)",
        title="Llama3-8B · Sarathi · RTX 3090\nShareGPT · BS256 · 1200 MHz · rep1",
    )
    if full_range:
        ax.set_ylim(0, float(y.max()) * 1.08)
    else:
        limit = float(np.quantile(y, 0.99) * 1.15)
        over = y > limit
        ax.set_ylim(0, limit)
        if over.any():
            ax.scatter(x[over], np.full(over.sum(), limit * 0.98), marker="^",
                       c="#b23a32", s=32, label=f"{over.sum()} above view")
            ax.text(0.02, 0.96, f"Main-range view; {over.sum()} points above {limit:.1f} ms",
                    transform=ax.transAxes, va="top", fontsize=9)
    ax.grid(ls="--", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(loc="lower right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    suffix = "full_range" if full_range else "main_range"
    for extension in ("pdf", "png"):
        fig.savefig(HERE / f"{PREFIX}_{suffix}.{extension}", dpi=220)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("/home/hcw/LLM_pipeline_infer"))
    args = parser.parse_args()
    run = args.data_root / RUN_RELATIVE
    points, request_count = load_points(run)
    write_csv(HERE / "raw_selected_batches.csv", points,
              ("batch_id", "requests", "context_tokens", "middle_stage_ms"))
    grouped = collections.defaultdict(list)
    for point in points:
        grouped[point["context_tokens"]].append(point["middle_stage_ms"])
    means = [
        {"context_tokens": tokens, "middle_stage_ms": float(np.mean(values)), "count": len(values)}
        for tokens, values in sorted(grouped.items())
    ]
    write_csv(HERE / "exact_x_means.csv", means,
              ("context_tokens", "middle_stage_ms", "count"))
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11})
    draw(means, request_count, full_range=False)
    draw(means, request_count, full_range=True)
    (HERE / "method.json").write_text(json.dumps({
        "source": str(RUN_RELATIVE),
        "setting": "1200 MHz on stages 0–2; last stage Auto",
        "repeat": 1,
        "request_count": request_count,
        "selected_batches": len(points),
        "exact_x_points": len(means),
        "selection": "pure decode with modal request count",
        "x": "sum of request context lengths before this decode batch",
        "y": "mean CUDA Event stage duration of stages 1 and 2",
        "aggregation": "mean of batches with exactly equal x; no smoothing or duration filtering",
        "checks": "stage batch IDs and request metadata match; reconstructed prompt and decode counts match output summaries",
    }, indent=2) + "\n")
    print(f"Saved {len(points)} batches, {len(means)} x values; {request_count} requests per batch")


if __name__ == "__main__":
    main()
