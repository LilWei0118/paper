# Selected paper figures and tables

This folder keeps copies of the current PNG/PDF figure previews. The manuscript's `\includegraphics` paths have not been changed. Run `python sync.py` here after updating a source figure to refresh the copies; the script verifies that every copy matches its source in `../hcw_figures/`.

Tick marks point into the plot on numeric horizontal and vertical axes. Fig. 3 uses model names on the horizontal axis, so its horizontal tick marks are hidden. The right-hand vertical axis in Fig. 11 also uses inward tick marks.
Model labels in the figures show model names only; framework and GPU details remain in the source documentation.
Every plotting area has a closed four-sided border, including Fig. 11's dual-axis panels.

| Figure | Current version | Selection |
|---|---|---|
| Fig. 3 | [PNG](Fig3_auto_stage_idle_sharegpt_bs256_20261017.png) · [PDF](Fig3_auto_stage_idle_sharegpt_bs256_20261017.pdf) | ShareGPT, BS256, Qwen3-8B and Llama3-70B only |
| Fig. 4 | [PNG](Fig4_auto_context_main_range_20261017.png) · [PDF](Fig4_auto_context_main_range_20261017.pdf) | ShareGPT, Qwen3-8B above Llama3-70B, sequence length 0–15,000; shorter panels crop lower blank space while retaining the data scale |
| Fig. 6 | [PNG](Fig6_power_sarathi_20261017.png) · [PDF](Fig6_power_sarathi_20261017.pdf) | Sarathi Llama3-8B, ShareGPT BS256, samples 100–680, near-square layout |
| Fig. 7 | [PNG](Fig7_frequency_stage_time_llama_sharegpt_20261018.png) · [PDF](Fig7_frequency_stage_time_llama_sharegpt_20261018.pdf) | ShareGPT, Llama3-8B and Llama3-70B |
| Fig. 9 | [PNG](Fig9_energy_performance_three_models_output2_20261017.png) · [PDF](Fig9_energy_performance_three_models_output2_20261017.pdf) | Three models, signed values labeled on bars |
| Fig. 10 | [PNG](Fig10_math_total_bubble_reduction_three_models_20261018.png) · [PDF](Fig10_math_total_bubble_reduction_three_models_20261018.pdf) | MATH, three panels in one figure, total inter-batch gap-duration reduction |
| Fig. 11 | [PNG](Fig11_sharegpt_three_models_bs256_output2_20261018.png) · [PDF](Fig11_sharegpt_three_models_bs256_output2_20261018.pdf) | ShareGPT BS256, actual total energy and inference time, no Auto point |
| Fig. 12 | [PNG](Fig12_random_four_point_fit_sharegpt_output2_20261018.png) · [PDF](Fig12_random_four_point_fit_sharegpt_output2_20261018.pdf) | ShareGPT, three vertically stacked models, four random fit points and five held-out points per curve; all markers and lines solid |

Only the ShareGPT three-model version is kept as the current Fig. 12 preview. It accompanies the two tables below. All Fig. 12 curves display nine measured frequency points. For A100, 870 MHz is omitted consistently to reduce its ten measured frequencies to nine.

**Table 1** ([Markdown](Table1_sharegpt_stage_alignment.md), [CSV](Table1_sharegpt_stage_alignment.csv)) gives nine continuous frequencies where each ShareGPT Fig. 12 middle-stage fitted curve equals the final stage's Auto mean decode time. They are stage-time alignment estimates, not measured energy-optimal settings. The [calculation script](../hcw_figures/fig12_random_four_point_fit_20261018/stage_alignment.py) is preserved with the source data.

**Table 2** ([Markdown](Table2_sharegpt_nine_point_mape.md), [CSV](Table2_sharegpt_nine_point_mape.csv)) gives one MAPE per ShareGPT curve, averaged over all nine displayed measurements (four fitting points and five held-out points). The CSV also reports the fitting-only and validation-only MAPE values. The [calculation script](../hcw_figures/fig12_random_four_point_fit_20261018/sharegpt_mape.py) is preserved with the source data.
