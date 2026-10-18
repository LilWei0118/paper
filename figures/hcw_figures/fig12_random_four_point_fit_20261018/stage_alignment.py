#!/usr/bin/env python3
"""Solve ShareGPT middle-stage/Auto last-stage crossing frequencies."""

import csv
import math
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
MODELS = (
    ("sarathi", "Llama3-8B", (64, 128, 256)),
    ("qwen", "Qwen3-8B", (64, 128, 256)),
    ("a100", "Llama3-70B", (128, 256, 512)),
)


def read_csv(name):
    with (HERE / name).open(newline="") as file:
        return list(csv.DictReader(file))


def main():
    fits = {(row["model"], int(row["bs"])): row
            for row in read_csv("fit_coefficients.csv")
            if row["dataset"] == "sharegpt"}
    stages = defaultdict(list)
    for row in read_csv("last_stage_auto_sharegpt.csv"):
        assert row["dataset"] == "sharegpt"
        stages[(row["model"], int(row["bs"]))].append(row)
    scans = defaultdict(list)
    for row in read_csv("measured_predicted.csv"):
        if row["dataset"] == "sharegpt":
            scans[(row["model"], int(row["bs"]))].append(int(row["frequency_mhz"]))
    assert len(fits) == len(stages) == len(scans) == 9

    results = []
    for model, name, sizes in MODELS:
        for bs in sizes:
            key = (model, bs)
            fit, runs = fits[key], stages[key]
            assert len(runs) == (1 if model == "a100" else 2)
            assert sorted(int(row["repeat"]) for row in runs) == list(range(1, len(runs) + 1))
            target = sum(float(row["stage_time_ms"]) for row in runs) / len(runs)
            amplitude = float(fit["shifted_amplitude"])
            rate = float(fit["k2"])
            floor = float(fit["k3"])
            offset = float(fit["offset_mhz"])
            if amplitude <= 0 or rate <= 0 or not floor < target < floor + amplitude:
                raise ValueError(f"No finite positive crossing for {name}, BS{bs}")
            frequency = offset - math.log((target - floor) / amplitude) / rate
            low, high = min(scans[key]), max(scans[key])
            if not low <= frequency <= high:
                raise ValueError(f"Crossing outside scanned range for {name}, BS{bs}: {frequency}")
            predicted = amplitude * math.exp(-rate * (frequency - offset)) + floor
            assert math.isclose(predicted, target, rel_tol=1e-12, abs_tol=1e-12)
            results.append({"model": name, "dataset": "ShareGPT", "bs": bs,
                            "last_stage_auto_ms": target,
                            "crossing_frequency_mhz": frequency,
                            "fit_frequencies_mhz": fit["fit_frequencies_mhz"],
                            "scan_min_mhz": low, "scan_max_mhz": high,
                            "last_stage_repeats": len(runs)})

    with (HERE / "sharegpt_stage_alignment.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    by_key = {(row["model"], row["bs"]): row["crossing_frequency_mhz"]
              for row in results}
    lines = ["# ShareGPT fitted stage-time alignment", "",
             "Intersection frequency in MHz; the values are continuous fitted estimates.", "",
             "| Model | BS64 | BS128 | BS256 | BS512 |",
             "|---|---:|---:|---:|---:|"]
    for _, name, _ in MODELS:
        cells = [f"{by_key[(name, bs)]:.1f}" if (name, bs) in by_key else "—"
                 for bs in (64, 128, 256, 512)]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    lines.extend(["", "The target is the mean Auto decode time of the final stage "
                  "(stage 3 for the 8B models; stage 7 for Llama3-70B). "
                  "The fitted curve represents the mean intermediate-stage decode time. "
                  "See the CSV for unrounded frequencies, targets, and selected fit points.", ""])
    (HERE / "sharegpt_stage_alignment.md").write_text("\n".join(lines))
    print(f"Saved {len(results)} ShareGPT crossing frequencies")


if __name__ == "__main__":
    main()
