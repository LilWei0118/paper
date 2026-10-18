#!/usr/bin/env python3
"""Fig. 6: measured RTX 3090 power for Llama3-8B/Sarathi/ShareGPT/BS256."""

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
OUTPUT = HERE.parent / "Fig6_power_sarathi_20261017"
SOURCE = Path("/home/hcw/LLM_pipeline_infer/dataset_runs/"
              "sarathi_llama3_8b_3090_freq_bs64_128_256/sharegpt/bs256/scan")
SETTINGS = ("auto", "freq1800", "freq1200", "freq900", "freq600")
COLORS = ("#232323", "#0072B2", "#009E73", "#E69F00", "#CC79A7")
GPU_INDEX = 5  # Physical RTX 3090, nonfinal pipeline Stage 1.
SAMPLE_RANGE = (100, 400)


def extract():
    samples, summary = [], []
    for setting in SETTINGS:
        run = SOURCE / setting / "rep1"
        measurement = json.loads((run / "measurement.json").read_text())
        assert measurement["dataset"] == "sharegpt" and measurement["bs"] == 256
        start = measurement["start_monotonic_ns"]
        end = measurement["end_monotonic_ns"]
        selected = []
        with (run / "telemetry.csv").open(newline="") as file:
            for row in csv.DictReader(file):
                timestamp = int(row["monotonic_ns"])
                if int(row["index"]) != GPU_INDEX or not start <= timestamp <= end:
                    continue
                power = row["power.draw.instant"]
                if power:
                    selected.append(dict(setting=setting, sample=len(selected),
                                         elapsed_s=(timestamp - start) / 1e9,
                                         power_w=float(power),
                                         sm_clock_mhz=float(row["clocks.current.sm"])))
        assert len(selected) >= 50, (setting, len(selected))
        samples.extend(selected)
        summary.append(dict(setting=setting, dataset="sharegpt", bs=256, repeat=1,
                            stage=1, gpu_index=GPU_INDEX, samples=len(selected),
                            mean_power_w=sum(row["power_w"] for row in selected) / len(selected),
                            inference_time_s=measurement["inference_time_s"],
                            source=str(run / "telemetry.csv")))
    for name, rows in (("power_samples.csv", samples), ("trace_summary.csv", summary)):
        with (HERE / name).open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def load():
    with (HERE / "power_samples.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    traces = {setting: [] for setting in SETTINGS}
    for row in rows:
        traces[row["setting"]].append((int(row["sample"]), float(row["power_w"])))
    assert all(len(trace) >= 50 for trace in traces.values())
    assert all([sample for sample, _ in trace] == list(range(len(trace)))
               for trace in traces.values())
    return traces


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-data", action="store_true",
                        help="Re-extract CSV snapshots from the local raw experiment")
    args = parser.parse_args()
    if args.refresh_data:
        extract()
    traces = load()
    assert all(len(trace) > SAMPLE_RANGE[1] for trace in traces.values())
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11})
    fig, ax = plt.subplots(figsize=(8.2, 3.7))
    for setting, color in zip(SETTINGS, COLORS):
        trace = traces[setting]
        label = "Auto" if setting == "auto" else setting.removeprefix("freq") + " MHz"
        ax.plot([sample for sample, _ in trace], [power for _, power in trace],
                lw=1.15, color=color, alpha=0.9, label=label)
    top = 25 * math.ceil(max(power for trace in traces.values()
                             for sample, power in trace
                             if SAMPLE_RANGE[0] <= sample <= SAMPLE_RANGE[1]) / 25)
    ax.set(title="Llama3-8B",
           xlabel="Sample Times", ylabel="Power (W)",
           xlim=SAMPLE_RANGE, ylim=(0, top))
    ax.grid(ls="--", alpha=0.25)
    ax.legend(ncol=5, fontsize=8, loc="upper center", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTPUT.with_suffix(".png"), dpi=220, bbox_inches="tight")
    fig.savefig(OUTPUT.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {OUTPUT}.png and .pdf; sample counts: " +
          ", ".join(f"{setting}={len(traces[setting])}" for setting in SETTINGS))


if __name__ == "__main__":
    main()
