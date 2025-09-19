import numpy as np
from typing import Tuple

def normalize_pdf(pdf: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Normalize a PDF defined on grid x."""
    area = np.trapz(pdf, x)
    if area <= 0:
        raise ValueError('non-positive area in pdf normalization')
    return pdf / area


def safe_log(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    return np.log(np.maximum(x, eps))