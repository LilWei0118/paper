#!/usr/bin/env python3
"""Reproduce Fig. 12 from the checked-in stage-time measurements."""

import csv
import hashlib
import random
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
FIGURES = HERE.parent
SEED = 20261018
MODELS = (
    ("sarathi", "Llama3-8B", (64, 128, 256)),
    ("qwen", "Qwen3-8B", (64, 128, 256)),
    ("a100", "Llama3-70B", (128, 256, 512)),
)
COLORS = ("#dec464", "#d76677", "#76c5e9")
FIELDS = ("model", "dataset", "bs", "frequency_mhz", "measured_stage_ms",
          "repeats", "provisional", "source")


def read_measurements():
    with (HERE / "measurements.csv").open(newline="") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 252
    assert tuple(rows[0]) == FIELDS
    for row in rows:
        row["bs"] = int(row["bs"])
        row["frequency_mhz"] = int(row["frequency_mhz"])
        row["measured_stage_ms"] = float(row["measured_stage_ms"])
        row["repeats"] = int(row["repeats"])
        row["provisional"] = row["provisional"] == "True"
    # A100 has ten tested clocks. Drop the same interior clock for every A100
    # configuration to show nine measurements per curve while retaining endpoints.
    return [row for row in rows if not (row["model"] == "a100"
                                       and row["frequency_mhz"] == 870)]


def write_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fit_exp(rows):
    """Fit T=a exp[-b(f-fmin)]+c; same bounded search as prior Fig. 12."""
    f = np.array([row["frequency_mhz"] for row in rows], dtype=float)
    y = np.array([row["measured_stage_ms"] for row in rows], dtype=float)
    offset = float(min(f))

    def objective(log_b):
        b = float(np.exp(log_b))
        x = np.exp(-b * (f - offset))
        a, c = np.linalg.lstsq(np.column_stack((x, np.ones_like(x))), y, rcond=None)[0]
        if a < 0 or c < 0:
            return float("inf"), a, c
        return float(np.sum((a * x + c - y) ** 2)), float(a), float(c)

    candidates = np.linspace(np.log(1e-5), np.log(0.05), 1601)
    scores = [objective(value)[0] for value in candidates]
    index = int(np.argmin(scores))
    lo = candidates[max(0, index - 1)]
    hi = candidates[min(len(candidates) - 1, index + 1)]
    phi = (np.sqrt(5) - 1) / 2
    u, v = hi - phi * (hi - lo), lo + phi * (hi - lo)
    for _ in range(75):
        if objective(u)[0] <= objective(v)[0]:
            hi, v = v, u
            u = hi - phi * (hi - lo)
        else:
            lo, u = u, v
            v = lo + phi * (hi - lo)
    b = float(np.exp((lo + hi) / 2))
    score, a, c = objective(np.log(b))
    if not np.isfinite(score):
        raise ValueError("Exponential fit failed")
    return {"k1": float(a * np.exp(b * offset)), "k2": b, "k3": c,
            "offset_mhz": offset, "shifted_amplitude": a}


def choose_frequencies(model, dataset, bs, rows):
    key = f"{SEED}:{model}:{dataset}:{bs}".encode()
    group_seed = int.from_bytes(hashlib.sha256(key).digest()[:8], "big")
    rng = random.Random(group_seed)
    return set(rng.sample(sorted(row["frequency_mhz"] for row in rows), 4))


def prepare(measured):
    groups = defaultdict(list)
    for row in measured:
        groups[(row["model"], row["dataset"], row["bs"])].append(row)
    fits = []
    for (model, dataset, bs), rows in sorted(groups.items()):
        expected = 9
        if len(rows) != expected or len({row["frequency_mhz"] for row in rows}) != expected:
            raise ValueError(f"Incomplete scan: {model} {dataset} BS{bs}")
        selected = choose_frequencies(model, dataset, bs, rows)
        train = [row for row in rows if row["frequency_mhz"] in selected]
        validation = [row for row in rows if row["frequency_mhz"] not in selected]
        assert len(train) == 4 and len(validation) == 5
        fit = fit_exp(train)
        for row in rows:
            f = row["frequency_mhz"]
            row["role"] = "fit" if f in selected else "validation"
            row["predicted_stage_ms"] = float(
                fit["shifted_amplitude"] * np.exp(-fit["k2"] * (f - fit["offset_mhz"])) + fit["k3"])
            row["absolute_percentage_error"] = float(
                abs(row["predicted_stage_ms"] / row["measured_stage_ms"] - 1) * 100)
        fits.append({"model": model, "dataset": dataset, "bs": bs,
                     "random_seed": SEED, **fit,
                     "fit_frequencies_mhz": ",".join(map(str, sorted(selected))),
                     "validation_frequencies_mhz": ",".join(
                         str(row["frequency_mhz"]) for row in sorted(validation,
                                                key=lambda row: row["frequency_mhz"])),
                     "fit_points": len(train), "validation_points": len(validation),
                     "fit_mape_pct": float(np.mean([row["absolute_percentage_error"] for row in train])),
                     "validation_mape_pct": float(np.mean([
                         row["absolute_percentage_error"] for row in validation])),
                     "provisional": model == "a100" and dataset == "sharegpt" and bs == 512})
    if len(fits) != 27:
        raise ValueError(f"Expected 27 model/dataset/batch configurations, got {len(fits)}")
    return fits


def panel(ax, model, dataset, sizes, measured, fit_map, compact=False):
    for color, bs in zip(COLORS, sizes):
        rows = sorted((row for row in measured if row["model"] == model
                       and row["dataset"] == dataset and row["bs"] == bs),
                      key=lambda row: row["frequency_mhz"])
        fit = fit_map[(model, dataset, bs)]
        frequencies = np.array([row["frequency_mhz"] for row in rows])
        fine = np.linspace(min(frequencies), max(frequencies), 240)
        curve = fit["shifted_amplitude"] * np.exp(-fit["k2"] *
                (fine - fit["offset_mhz"])) + fit["k3"]
        ax.plot(fine, curve, color=color, lw=1.8)
        ax.scatter([row["frequency_mhz"] for row in rows],
                   [row["measured_stage_ms"] for row in rows], color=color,
                   s=27 if compact else 34, zorder=3, label=f"BS{bs}")
    ax.grid(ls="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(True)
    ax.tick_params(axis="both", which="both", direction="in",
                   labelsize=9 if compact else 10.5)
    ax.legend(fontsize=8.5 if compact else 10.5, ncol=3, loc="upper right")
    ax.set_xlim(left=min(row["frequency_mhz"] for row in measured
                         if row["model"] == model) - 20)
    ax.set_ylim(bottom=0)


def save(fig, stem):
    for suffix in ("png", "pdf"):
        fig.savefig(FIGURES / f"{stem}.{suffix}",
                    **({"dpi": 220} if suffix == "png" else {}))
    plt.close(fig)


def main():
    measured = read_measurements()
    fits = prepare(measured)
    write_csv(HERE / "measured_predicted.csv", measured)
    write_csv(HERE / "fit_coefficients.csv", fits)
    fit_map = {(row["model"], row["dataset"], row["bs"]): row for row in fits}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.labelsize": 11})

    fig, axes = plt.subplots(3, 1, figsize=(9.2, 9.0))
    for ax, (model, name, sizes) in zip(axes, MODELS):
        panel(ax, model, "sharegpt", sizes, measured, fit_map)
        ax.set_title(name, fontsize=15, pad=9)
        ax.set_xlabel("Frequency (MHz)", fontsize=13.5)
        ax.set_ylabel("T (ms)")
    fig.subplots_adjust(left=0.11, right=0.89, top=0.90, bottom=0.075, hspace=0.57)
    save(fig, "Fig12_random_four_point_fit_sharegpt_output2_20261018")
    print("Saved ShareGPT Fig. 12; retained fit records for 27 configurations")


if __name__ == "__main__":
    main()
