import json
from ref_toolkit.sim.neuromorphic_diagram import compute_critical_g_rel


def test_neuromorphic_stub():
    alpha, gcrit = compute_critical_g_rel()
    assert len(alpha) == len(gcrit)
    assert gcrit.min() >= 0.2