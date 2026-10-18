# Fig. 6: Llama3-8B / Sarathi / RTX 3090 / ShareGPT / BS256

`../Fig6_power_sarathi_20261017.png` and `.pdf` show the five rep1 traces:
Auto, 1800, 1200, 900, and 600 MHz. The x-axis label is “Sample Times” and
denotes the sample index within each run's inference window; the y axis is
measured instantaneous GPU power in watts. The plotted interval is sample
indices 100–680, with no plot title. All five measured traces cover this
interval; the shortest trace ends at index 682. Curves are not smoothed or aligned in
time. The CSV preserves the full inference traces.
The PDF uses the same 8 × 7.27 inch page size as Fig. 7 for equal-width
placement in adjacent LaTeX minipages. The five-frequency legend is below the
plot in one row.

Samples come from physical RTX 3090 GPU index 5, pipeline Stage 1, and are
restricted to the `measurement.json` inference start/end timestamps. The
source is `/home/hcw/LLM_pipeline_infer/dataset_runs/`
`sarathi_llama3_8b_3090_freq_bs64_128_256/sharegpt/bs256/scan/`, rep1.
`power_samples.csv` stores the plotted values; `trace_summary.csv` records
run provenance and summary statistics.

Run `python plot.py` to rebuild PNG/PDF from the included CSV. Run
`python plot.py --refresh-data` on the experiment machine to extract fresh
samples from the original telemetry before plotting. The paper's LaTeX source
references this selected preview.
