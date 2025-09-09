import numpy as np

def normalize_pdf(pdf, x):
    """Normalize a PDF defined on grid x."""
    area = np.trapz(pdf, x)
    if area <= 0:
        raise ValueError('non-positive area in pdf normalization')
    return pdf / area


def safe_log(x, eps=1e-12):
    return np.log(np.maximum(x, eps))