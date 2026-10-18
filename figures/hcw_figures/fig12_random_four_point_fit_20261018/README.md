# Fig. 12: four-point fits with nine measurements per curve

Run `python plot.py` to regenerate the atlas and the ShareGPT, MATH, and Natural Questions PNG/PDF figures in the parent directory. The script uses only the checked-in `measurements.csv` and records every prediction and selected frequency in `measured_predicted.csv` and `fit_coefficients.csv`.

Each of the 27 model–dataset–batch-size curves shows nine measured fixed-frequency points. A stable per-configuration seed, derived from master seed `20261018`, selects **four** of those points uniformly without replacement for an unweighted fit of `T = k1 exp(-k2 f) + k3`. The other **five** points are used for held-out validation. All nine points appear as solid markers, and every fitted curve is solid. The fit/validation distinction remains in the CSV, not in the plotted marker style. The reported validation MAPE is calculated only from the five held-out points. The overall mean validation MAPE across the 27 configurations is 7.27% for this one seeded split.

The two 8B models have nine measured fixed frequencies. A100 has ten; to show the same number for all models, 870 MHz is excluded from **every** A100 curve before random selection. Both ends of the A100 frequency range remain visible. The original 870 MHz measurements are preserved in `measurements.csv`, but are not fitted, plotted, or counted in validation. Auto is excluded because it has no single fixed frequency.

The measurements are a snapshot of the earlier Fig. 12 scan: intermediate decode stages 1–2 for the RTX 3090 models and stages 1–6 for A100, averaged within each run. The 8B measurements average two runs per setting; A100 uses one run. The A100 ShareGPT BS512 source has incomplete raw stage files; this limitation remains recorded as `provisional=True` in the CSV. Held-out points are from the same frequency scans, not separate experimental runs.

The earlier five-point and all-point versions remain in the parent directory. The manuscript's LaTeX figure reference is unchanged.
