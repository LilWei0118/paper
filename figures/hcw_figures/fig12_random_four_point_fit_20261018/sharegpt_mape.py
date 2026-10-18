#!/usr/bin/env python3
"""Calculate nine-measurement MAPE for each ShareGPT Fig. 12 curve."""

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
    groups = defaultdict(list)
    for row in read_csv("measured_predicted.csv"):
        if row["dataset"] == "sharegpt":
            groups[(row["model"], int(row["bs"]))].append(row)
    fits = {(row["model"], int(row["bs"])): row
            for row in read_csv("fit_coefficients.csv")
            if row["dataset"] == "sharegpt"}
    assert len(groups) == len(fits) == 9

    results = []
    for model, name, sizes in MODELS:
        for bs in sizes:
            rows = groups[(model, bs)]
            assert len(rows) == 9
            assert len({int(row["frequency_mhz"]) for row in rows}) == 9
            assert sum(row["role"] == "fit" for row in rows) == 4
            assert sum(row["role"] == "validation" for row in rows) == 5
            errors = []
            for row in rows:
                measured = float(row["measured_stage_ms"])
                predicted = float(row["predicted_stage_ms"])
                assert measured > 0
                error = abs(predicted - measured) / measured * 100
                assert math.isclose(error, float(row["absolute_percentage_error"]),
                                    rel_tol=1e-10, abs_tol=1e-10)
                errors.append(error)
            mape = sum(errors) / 9
            fit = fits[(model, bs)]
            weighted = (4 * float(fit["fit_mape_pct"]) +
                        5 * float(fit["validation_mape_pct"])) / 9
            assert math.isclose(mape, weighted, rel_tol=1e-10, abs_tol=1e-10)
            results.append({"model": name, "dataset": "ShareGPT", "bs": bs,
                            "points": 9, "fit_points": 4, "validation_points": 5,
                            "nine_point_mape_pct": mape,
                            "fit_mape_pct": float(fit["fit_mape_pct"]),
                            "validation_mape_pct": float(fit["validation_mape_pct"])})

    with (HERE / "sharegpt_nine_point_mape.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    by_key = {(row["model"], row["bs"]): row["nine_point_mape_pct"]
              for row in results}
    lines = ["# ShareGPT Fig. 12 nine-point MAPE", "",
             "Each percentage averages the absolute percentage errors at all nine "
             "measured frequencies on one fitted curve (four fit + five held-out points).", "",
             "| Model | BS64 | BS128 | BS256 | BS512 |",
             "|---|---:|---:|---:|---:|"]
    for _, name, _ in MODELS:
        cells = [f"{by_key[(name, bs)]:.2f}%" if (name, bs) in by_key else "—"
                 for bs in (64, 128, 256, 512)]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    lines.extend(["", "MAPE = (1/9) × Σ |predicted stage time − measured stage time| "
                  "/ measured stage time × 100%. "
                  "This all-point MAPE includes fitting points; see the CSV for "
                  "fit-only and held-out-only MAPE.", ""])
    (HERE / "sharegpt_nine_point_mape.md").write_text("\n".join(lines))
    print(f"Saved {len(results)} ShareGPT nine-point MAPE values")


if __name__ == "__main__":
    main()
