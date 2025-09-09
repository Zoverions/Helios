"""Stable 1D Fokker-Planck solver and plotting for REF."""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from ..utils import normalize_pdf, safe_log


def fpe_rhs_stable(t, P, phi_grid, omega, g_rel, gamma, sigma):
    dphi = phi_grid[1] - phi_grid[0]
    safe_phi = np.maximum(phi_grid, 1e-9)
    # drift
    mu = -(omega**2 - g_rel) * safe_phi - gamma * (safe_log(safe_phi) + 1.0)
    # clip mu to prevent runaway terms in stiff regions
    mu = np.clip(mu, -1e6, 1e6)
    # diffusion
    D = (sigma * safe_phi)**2

    # Conservative upwind flux scheme (robust to singularity)
    J = np.zeros_like(phi_grid)
    # advective flux (upwind)
    adv_flux = np.zeros_like(phi_grid)
    adv_flux[1:] = np.where(mu[:-1] > 0, mu[:-1] * P[:-1], mu[1:] * P[1:])
    # diffusive flux (central-like difference but conservative)
    diff_flux = np.zeros_like(phi_grid)
    DP = D * P
    diff_flux[1:] = (DP[1:] - DP[:-1]) / dphi
    J = adv_flux - diff_flux

    # divergence of flux -> dP/dt
    dPdt = np.zeros_like(P)
    dPdt[1:-1] = -(J[2:] - J[1:-1]) / dphi
    # zero-flux boundary conditions (conservative)
    dPdt[0] = 0.0
    dPdt[-1] = 0.0
    return dPdt


def solve_fpe(phi_grid, P0, omega, g_rel, gamma, sigma, t_span=(0, 20)):
    sol = solve_ivp(
        fun=lambda t, y: fpe_rhs_stable(t, y, phi_grid, omega, g_rel, gamma, sigma),
        t_span=t_span,
        y0=P0,
        method='BDF',
        atol=1e-9,
        rtol=1e-6,
    )
    if not sol.success:
        raise RuntimeError('FPE solver failed: ' + sol.message)
    P_final = sol.y[:, -1]
    # ensure positivity and normalize
    P_final = np.clip(P_final, 0.0, None)
    P_final = normalize_pdf(P_final, phi_grid)
    return P_final


def compute_stats(phi_grid, P):
    mean = np.trapz(phi_grid * P, phi_grid)
    var = np.trapz(P * (phi_grid - mean)**2, phi_grid)
    std = np.sqrt(var)
    return mean, std


def run_fpe_analysis(out_file='fpe_evolution.png', mode='demo'):
    phi_grid = np.linspace(0.01, 2.0, 200)
    P0 = np.exp(-((phi_grid - 1.0)**2) / (2 * 0.1**2))
    P0 /= np.trapz(P0, phi_grid)

    if mode == 'hierarchical':
        omega, g_rel, gamma, sigma = 1.0, 0.5, 0.1, 0.02
    elif mode == 'uniform':
        omega, g_rel, gamma, sigma = 1.0, 0.0, 0.1, 0.02
    else:
        # demo toggles between both and overlays
        omega, g_rel, gamma, sigma = 1.0, 0.5, 0.1, 0.02

    P_final = solve_fpe(phi_grid, P0, omega, g_rel, gamma, sigma)
    mean, std = compute_stats(phi_grid, P_final)

    # If demo, also compute uniform for comparison
    if mode == 'demo':
        P_uni = solve_fpe(phi_grid, P0, 1.0, 0.0, gamma, sigma)
        mean_u, std_u = compute_stats(phi_grid, P_uni)

    plt.figure(figsize=(8, 6))
    plt.plot(phi_grid, P_final, label=f'Hierarchical (σ={std:.3f})')
    if mode == 'demo':
        plt.plot(phi_grid, P_uni, linestyle='--', label=f'Uniform (σ={std_u:.3f})')
    plt.xlabel('Order Parameter (φ)')
    plt.ylabel('Probability Density P(φ)')
    plt.legend(); plt.grid(True); plt.title('FPE: Stationary Distributions')
    plt.savefig(out_file, dpi=300)
    plt.close()

    return {'phi': phi_grid, 'P': P_final, 'mean': mean, 'std': std}