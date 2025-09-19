import pytest
import numpy as np
from ref_toolkit.analytics.ref_fpe_1d import solve_fpe, compute_stats


def test_fpe_converges():
    phi_grid = np.linspace(0.01, 2.0, 100)
    P0 = np.exp(-((phi_grid - 1.0)**2) / (2 * 0.1**2))
    P0 /= np.trapz(P0, phi_grid)
    P_final = solve_fpe(phi_grid, P0, omega=1.0, g_rel=0.5, gamma=0.1, sigma=0.02)
    assert np.all(P_final >= 0.0)
    mean, std = compute_stats(phi_grid, P_final)
    assert std > 0.0


def test_fpe_normalization():
    phi_grid = np.linspace(0.01, 2.0, 100)
    P0 = np.exp(-((phi_grid - 1.0)**2) / (2 * 0.1**2))
    P0 /= np.trapz(P0, phi_grid)
    P_final = solve_fpe(phi_grid, P0, omega=1.0, g_rel=0.0, gamma=0.1, sigma=0.02)
    area = np.trapz(P_final, phi_grid)
    assert pytest.approx(area, rel=1e-6) == 1.0


def test_fpe_edge_case_zero_sigma():
    phi_grid = np.linspace(0.01, 2.0, 100)
    P0 = np.exp(-((phi_grid - 1.0)**2) / (2 * 0.1**2))
    P0 /= np.trapz(P0, phi_grid)
    with pytest.raises(RuntimeError):
        solve_fpe(phi_grid, P0, omega=1.0, g_rel=0.5, gamma=0.1, sigma=0.0)


def test_compute_stats():
    phi_grid = np.linspace(0.01, 2.0, 100)
    P = np.exp(-((phi_grid - 1.0)**2) / (2 * 0.1**2))
    P /= np.trapz(P, phi_grid)
    mean, std = compute_stats(phi_grid, P)
    assert mean > 0
    assert std > 0