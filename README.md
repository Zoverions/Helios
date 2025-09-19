# Helios (ref_toolkit) — v2.0

Helios is the companion toolkit for the Resonant Entropy Field (REF) project. It reproduces the 1D Fokker-Planck figure, provides a neuromorphic phase-diagram stub, and includes a small CLI.

## Installation

```bash
pip install -e .[dev]
```

## Quickstart

```bash
# Run Fokker-Planck analysis
ref-fpe --mode demo --out fpe_evolution.png

# Run neuromorphic simulation
ref-sim --chip dynapse-se2 --out phase_diagram.json
```

## CLI Commands

### ref-fpe

Run the Fokker-Planck equation solver for stationary distributions.

Options:
- `--out`: Output filename for the plot (default: fpe_evolution.png)
- `--mode`: Preset mode - 'demo', 'hierarchical', or 'uniform' (default: demo)

### ref-sim

Run the neuromorphic phase diagram simulation.

Options:
- `--chip`: Chip model (default: dynapse-se2)
- `--out`: Output filename for JSON results (default: phase_diagram.json)

## API

### Analytics

- `run_fpe_analysis(out_file, mode)`: Solves FPE and saves plot.

### Simulation

- `compute_critical_g_rel(alpha_grid)`: Computes critical g_rel values.

### Utils

- `normalize_pdf(pdf, x)`: Normalizes a PDF.
- `safe_log(x, eps)`: Safe logarithm with epsilon.

## Development

Run tests: `pytest`

Contributions welcome. MIT license.