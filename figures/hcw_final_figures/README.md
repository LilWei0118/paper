# Selected paper figures and tables

This folder keeps copies of the current PNG/PDF figure previews. The manuscript's `\includegraphics` paths have not been changed. Run `python sync.py` here after updating a source figure to refresh the copies; the script verifies that every copy matches its source in `../hcw_figures/`.

| Figure | Current version | Selection |
|---|---|---|
| Fig. 3 | `Fig3_auto_stage_idle_sharegpt_bs256_20261017.{png,pdf}` | ShareGPT, BS256, Qwen3-8B and Llama3-70B only |
| Fig. 4 | `Fig4_auto_context_main_range_20261017.{png,pdf}` | ShareGPT, Qwen3-8B above Llama3-70B, sequence length 0–15,000 |
| Fig. 6 | `Fig6_power_sarathi_20261017.{png,pdf}` | Sarathi Llama3-8B, ShareGPT BS256, samples 100–400 |
| Fig. 7 | `Fig7_frequency_stage_time_llama_sharegpt_20261018.{png,pdf}` | ShareGPT, Llama3-8B and Llama3-70B |
| Fig. 9 | `Fig9_energy_performance_three_models_output2_20261017.{png,pdf}` | Three models, signed values labeled on bars |
| Fig. 10 | `Fig10_math_total_bubble_reduction_three_models_20261018.{png,pdf}` | MATH, three panels in one figure, total inter-batch gap-duration reduction |
| Fig. 11 | `Fig11_sharegpt_three_models_bs256_output2_20261018.{png,pdf}` | ShareGPT BS256, actual total energy and inference time, no Auto point |
| Fig. 12 | `Fig12_random_four_point_fit_sharegpt_output2_20261018.{png,pdf}` | ShareGPT, three models, four random fit points and five held-out points per curve; all markers and lines solid |

The current Fig. 12 style is also copied for **MATH**, **Natural Questions**, and the **nine-panel atlas** under their corresponding `Fig12_random_four_point_fit_*_output2_20261018.{png,pdf}` names. The ShareGPT three-model version accompanies the two tables below. All Fig. 12 curves display nine measured frequency points. For A100, 870 MHz is omitted consistently to reduce its ten measured frequencies to nine.

**Table 1** is `Table1_sharegpt_stage_alignment.{md,csv}`: nine continuous frequencies where each ShareGPT Fig. 12 middle-stage fitted curve equals the final stage's Auto mean decode time. They are stage-time alignment estimates, not measured energy-optimal settings. The calculation script is `../hcw_figures/fig12_random_four_point_fit_20261018/stage_alignment.py`.

**Table 2** is `Table2_sharegpt_nine_point_mape.{md,csv}`: one MAPE per ShareGPT curve, averaged over all nine displayed measurements (four fitting points and five held-out points). The CSV also reports the fitting-only and validation-only MAPE values. The calculation script is `../hcw_figures/fig12_random_four_point_fit_20261018/sharegpt_mape.py`.
