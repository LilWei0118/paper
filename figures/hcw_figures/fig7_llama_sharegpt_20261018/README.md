# Fig. 7: two Llama models on ShareGPT

`../Fig7_frequency_stage_time_llama_sharegpt_20261018.png` and `.pdf` show
Llama3-8B/Sarathi/RTX 3090 above Llama3-70B/SGLang/A100. Run `python plot.py`
to regenerate them from the included CSV snapshots. The older
`Fig7_frequency_stage_time_three_models_sharegpt_20261017.*` preview name is
also updated with the same two-panel figure for existing links.

The plotted values come from the existing
`/home/hcw/LLM_pipeline_infer/analysis/fig7_frequency_stage_time_three_models_20261017/`
ShareGPT summary, filtered to the two Llama models. `sharegpt_per_run.csv`
preserves the corresponding per-run values. Each Llama3-8B point averages
the middle pipeline Stages 1–2 within each run, then equally averages two
repetitions. Each Llama3-70B point averages Stages 1–6 and has one repetition.
Auto is excluded because it has no single fixed clock. A100 uses the
`stage7_auto` dataset (formerly `output2`).

The panels show only model names in their titles, use "Frequency (MHz)" and
"T(ms)" as axis labels, and draw every batch-size series with a solid line.
For the A100 ShareGPT BS512 series, some original raw files were previously
flagged as missing. Its imported stage summaries still need validation
before using that series as a final quantitative claim; this provenance is
retained in the CSV even though the plot does not mark it separately. The
paper's LaTeX source does not yet reference this preview.
