# Fig. 11 atlas with actual energy

This script regenerates `../Fig11_all_configs_atlas_output2_20261017.png` and
`.pdf` from `values.csv`. The blue left axis is **measured total energy (kJ)**
for each Auto or capped-frequency setting. The red right axis is measured
inference time (s). The pale green band retains the Fig. 9 selected setting.
The two Y-axis display ranges leave space below the blue curve and above the
red curve so the curves do not cover each other; no measured values are changed.

`values.csv` is a snapshot of the measured and aggregated values in
`/home/hcw/LLM_pipeline_infer/analysis/fig11_all_configs_20261017/fig11_all_values.csv`.
Llama3-8B/Sarathi and Qwen3-8B/SGLang values are means of two full runs per
setting. Llama3-70B/SGLang/A100 values are one run per setting from output2
(`stage7_auto`). A100 ShareGPT BS512 remains marked provisional because its
aggregate is available but some underlying raw stage records are unreadable.

Run `python plot.py` from this folder to rebuild the atlas. The old
energy-saved version remains available in Git history. The earlier script in
the experiment analysis directory still generates that historical version;
use this script for the current atlas. This preview is not referenced by the
paper's LaTeX source.
