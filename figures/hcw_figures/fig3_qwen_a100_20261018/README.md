# Fig. 3 two-model preview

This version of `../Fig3_auto_stage_idle_sharegpt_bs256_20261017.png` and
`.pdf` retains only Qwen3-8B/SGLang/RTX 3090 and
Llama3-70B/SGLang/A100. Both use ShareGPT, BS256, and Auto frequency.
The values and three-bar styling are unchanged from the earlier preview.

`values.csv` is a snapshot of the two rows in
`/home/hcw/LLM_pipeline_infer/analysis/fig3_auto_stage_idle_20261017/fig3_auto_values_bs256.csv`.
Run `python plot.py` in this folder to regenerate both output files.

The bars use separate statistics: Other Stages and Last Stage are average
pure-decode compute durations; IDLE is the average gap between adjacent
pure-decode compute intervals on nonfinal stages. The bars should not be
summed. The paper's LaTeX source does not yet reference this preview.
