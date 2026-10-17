# Fig. 10 preview: full-run inter-batch bubble duration

This version compares **total inter-batch gap duration**, not gap fractions.
For each model/dataset/batch size, the selected frequency comes from the saved
Fig. 9 setting choices: minimum energy under the 5% inference-time limit.

For every measured run and every **middle pipeline stage** (Stage 1–2 for the
four-stage models; Stage 1–6 for the eight-stage model), the script sums the
nonnegative gaps from the end of one batch's CUDA compute interval to the
start of the next. It includes all measured batch modes: prefill/extend,
mixed, and pure decode. No gaps are discarded based on length. Gaps before
the first and after the last measured batch are excluded because those
boundaries cannot be directly read from the local GPU event timeline.

The total sums gaps across middle stages. For Llama3-8B/Sarathi and
Qwen3-8B/SGLang, each setting has two runs; the script averages their total
gap durations. Llama3-70B/SGLang/A100 has one run from `stage7_auto`
(formerly `output2`). The plotted percentage is:

`100 × (Auto mean total gap − selected mean total gap) / Auto mean total gap`.

This is a relative reduction in **seconds of observed inter-batch gaps**.
It is not the difference in gap fractions, nor total GPU-device idle time.
A100 ShareGPT BS512 is N/A because the selected run's Stage 3–6 records
cannot be decoded. The previous Fig. 10 preview is retained separately.

Run `python plot.py --data-root /home/hcw/LLM_pipeline_infer` to regenerate
the PDF, PNG, and per-run/summary CSVs. The experimental raw data are
outside the paper repository; the selected frequency table is saved here.
