# Fig. 4: Llama3-8B and Llama3-70B on ShareGPT

`../Fig4_auto_context_main_range_20261017.png` and `.pdf` show Llama3-8B
(Sarathi, RTX 3090) above Llama3-70B (SGLang, A100). The panels use the
same layout, colors, model-only titles, shared vertical label, and 0–15,000
horizontal span as the previous Qwen3-8B version. Their 8 × 7.27 inch PDF
page matches Fig. 3 for insertion at equal LaTeX widths. The earlier Qwen3-8B
two-panel preview is preserved as `../Fig4_auto_context_qwen_a100_20261017.*`.

Both series use ShareGPT, Auto frequency, repetition 1. The horizontal value
is the **sum of request context lengths in a pure-decode batch**, not the
context length of one request. The vertical value is the mean CUDA compute
duration of the intermediate pipeline stages. The batch sizes are 64, 128,
and 256 for Llama3-8B and 128, 256, and 512 for Llama3-70B. Equal horizontal
values are averaged in the source. The source snapshot contains 8,627 rows
from `/home/hcw/LLM_pipeline_infer/analysis/fig4_auto_context_20261017/exact_x_means.csv`.

Two Llama3-8B BS128 rows at 8,914 and 8,956 tokens have durations of 97.34
and 96.00 ms; the other Llama3-8B rows peak at 8.40 ms. For readability,
the plot caps its vertical range after identifying values above three times
their batch-size series median. The two clipped rows remain in `values.csv`
and appear as upward triangles at their original horizontal positions on the
upper plot edge. No rows are removed from the source snapshot. The y-axis
lower limits are 2.4 ms for Llama3-8B and 7.5 ms for Llama3-70B.

Run `python plot.py` here to regenerate the combined Fig. 4 and separate
model previews. The A100 source is `stage7_auto` (formerly `output2`).
