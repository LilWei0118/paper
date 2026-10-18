#!/usr/bin/env python3
"""Copy the selected paper figure previews and Table 1/2 data here."""

import hashlib
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hcw_figures"
FIGURES = (
    "Fig3_auto_stage_idle_sharegpt_bs256_20261017",
    "Fig4_auto_context_main_range_20261017",
    "Fig6_power_sarathi_20261017",
    "Fig7_frequency_stage_time_llama_sharegpt_20261018",
    "Fig9_energy_performance_three_models_output2_20261017",
    "Fig10_math_total_bubble_reduction_three_models_20261018",
    "Fig11_sharegpt_three_models_bs256_output2_20261018",
    "Fig12_random_four_point_fit_sharegpt_output2_20261018",
    "Fig12_random_four_point_fit_math_output2_20261018",
    "Fig12_random_four_point_fit_natural_questions_output2_20261018",
    "Fig12_random_four_point_fit_atlas_output2_20261018",
)
TABLE_SOURCE = SOURCE / "fig12_random_four_point_fit_20261018"
TABLES = {
    "sharegpt_stage_alignment.csv": "Table1_sharegpt_stage_alignment.csv",
    "sharegpt_stage_alignment.md": "Table1_sharegpt_stage_alignment.md",
    "sharegpt_nine_point_mape.csv": "Table2_sharegpt_nine_point_mape.csv",
    "sharegpt_nine_point_mape.md": "Table2_sharegpt_nine_point_mape.md",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).digest()


def copy_verified(source, destination):
    if not source.is_file():
        raise FileNotFoundError(source)
    if not destination.exists() or digest(source) != digest(destination):
        shutil.copy2(source, destination)
    assert digest(source) == digest(destination)


def main():
    for stem in FIGURES:
        for suffix in (".png", ".pdf"):
            name = stem + suffix
            copy_verified(SOURCE / name, HERE / name)
    for source_name, destination_name in TABLES.items():
        copy_verified(TABLE_SOURCE / source_name, HERE / destination_name)
    print(f"Verified {len(FIGURES)} PNG/PDF pairs and {len(TABLES)} table files")


if __name__ == "__main__":
    main()
