# Fig. 9: throughput bars aligned with inference time

Run `python plot.py` to regenerate `../Fig9_energy_performance_three_models_output2_20261017.png`
and `.pdf` from the included 27 selected configurations. The selection table
is copied from `/home/hcw/LLM_pipeline_infer/analysis/fig9_energy_performance_three_models_20261017/selected_settings.csv`.
Each fixed-frequency setting minimizes measured energy subject to inference
time ≤105% of its Auto baseline and energy below Auto. A100 uses `stage7_auto`
(formerly `output2`).

The green bars now show **throughput decrease**:
`100 × (1 − selected throughput / Auto throughput)`, which equals the negative
of `throughput_change_pct` in the CSV. Positive means throughput fell; negative
means it rose. Since output-token counts are equal across frequency settings,
these bars are always on the same side of zero as the orange inference-time
change bars. The CSV retains the original signed throughput change so the
data provenance remains clear. Blue bars still show energy-efficiency gain.

The A100 ShareGPT BS512 aggregate remains marked provisional with an asterisk;
the paper caption explains it. The bottom annotation has been removed, the
vertical axes read "Change Rate", and the panels are taller to fill more of the
two-column figure area.
Every bar is labeled with its signed percentage value, rounded to one decimal.
The paper's LaTeX source references the selected PDF.
The panel titles contain only dataset and model names; framework and GPU
details remain in this provenance note.
