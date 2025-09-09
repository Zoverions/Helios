"""Neuromorphic phase-diagram stub for Helios.
This script is intentionally lightweight and deterministic to allow fast CI testing.
It emits a small JSON summary and optionally a PNG phase diagram.
"""
import numpy as np
import json
import argparse


def compute_critical_g_rel(alpha_grid=None):
    if alpha_grid is None:
        alpha_grid = np.linspace(0.0, 1.0, 41)
    # toy deterministic mapping: critical g_rel increases with alpha nonlinearly
    g_crit = 0.2 + 0.6 * (alpha_grid**1.5)
    return alpha_grid, g_crit


def main(argv=None):
    parser = argparse.ArgumentParser(description='Neuromorphic diagram stub')
    parser.add_argument('--chip', type=str, default='dynapse-se2')
    parser.add_argument('--out', type=str, default='phase_diagram.json')
    args = parser.parse_args(argv)

    alpha, gcrit = compute_critical_g_rel()
    summary = {
        'chip': args.chip,
        'alpha_grid': alpha.tolist(),
        'g_crit': gcrit.tolist(),
        'critical_g_rel_estimate': float(np.mean(gcrit))
    }
    with open(args.out, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f'Wrote {args.out}')
    return 0

if __name__ == '__main__':
    main()