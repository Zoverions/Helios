from click.testing import CliRunner
from ref_toolkit.cli import main


def test_cli_fpe_demo():
    runner = CliRunner()
    res = runner.invoke(main, ['fpe', '--mode', 'demo', '--out', 'test_out.png'])
    assert res.exit_code == 0
    assert 'FPE analysis complete' in res.output