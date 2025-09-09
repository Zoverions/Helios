import click
from .analytics.ref_fpe_1d import run_fpe_analysis

@click.group()
def main():
    """Helios command-line interface."""
    pass

@main.command('fpe')
@click.option('--out', default='fpe_evolution.png', help='Output filename for the FPE figure')
@click.option('--mode', default='demo', type=click.Choice(['demo','hierarchical','uniform']), help='Which preset to run')
def fpe(out, mode):
    """Run the Fokker-Planck analysis and save a figure."""
    run_fpe_analysis(out, mode=mode)
    click.echo(f'FPE analysis complete — saved {out}')

if __name__ == '__main__':
    main()