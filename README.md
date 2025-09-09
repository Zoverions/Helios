# Helios (ref_toolkit) — v1.0

Helios is the companion toolkit for the Resonant Entropy Field (REF) project. It reproduces the 1D Fokker-Planck figure, provides a neuromorphic phase-diagram stub, and includes a small CLI.

## Quickstart

```bash
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
ref-fpe --mode demo --out fpe_evolution.png
ref-sim --chip dynapse-se2 --out phase_diagram.json
```

Contributions welcome. MIT license.