import click
from .analytics.ref_fpe_1d import run_fpe_analysis
from .sim.neuromorphic_diagram import compute_critical_g_rel
import json
from typing import Any


@click.group()
def main() -> None:
    """Helios command-line interface."""
    pass

@main.command('fpe')
@click.option('--out', default='fpe_evolution.png', help='Output filename for the FPE figure')
@click.option('--mode', default='demo', type=click.Choice(['demo','hierarchical','uniform']), help='Which preset to run')
def fpe(out: str, mode: str) -> None:
    """Run the Fokker-Planck analysis and save a figure."""
    try:
        run_fpe_analysis(out, mode=mode)
        click.echo(f'FPE analysis complete — saved {out}')
    except Exception as e:
        click.echo(f'Error in FPE analysis: {e}', err=True)
        raise click.Abort()

@main.command('sim')
@click.option('--chip', default='dynapse-se2', help='Neuromorphic chip model')
@click.option('--out', default='phase_diagram.json', help='Output filename for the phase diagram JSON')
def sim(chip: str, out: str) -> None:
    """Run the neuromorphic phase diagram simulation and save results."""
    try:
        alpha, gcrit = compute_critical_g_rel()
        summary: dict[str, Any] = {
            'chip': chip,
            'alpha_grid': alpha.tolist(),
            'g_crit': gcrit.tolist(),
            'critical_g_rel_estimate': float(alpha.mean())
        }
        with open(out, 'w') as f:
            json.dump(summary, f, indent=2)
        click.echo(f'Neuromorphic simulation complete — saved {out}')
    except Exception as e:
        click.echo(f'Error in simulation: {e}', err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()