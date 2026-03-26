"""
theoTracing.m -> theo_tracing.py

Alternative boundary tracing implementation (debug/experimental version).
Uses get_theo_neighbourhood instead of get_neighbourhood.
"""

import numpy as np
from .get_theo_neighbourhood import get_theo_neighbourhood


def theo_tracing(region):
    """
    Trace boundaries using the alternative theo neighbourhood method.

    Parameters
    ----------
    region : np.ndarray
        Binary image (values 0 and 1).

    Returns
    -------
    B : list of np.ndarray
        List of boundary arrays, each of shape (N, 2) with [row, col] coordinates.
    L : list
        Placeholder.
    """
    B = []
    L = []

    trace_region = region.copy()
    x, y = region.shape
    marker = np.zeros((x, y), dtype=np.int32)

    numcells = 0

    for i in range(x):
        for j in range(y):
            if j + 1 < y and i + 1 < x:
                if (trace_region[i, j + 1] == 0 and
                        trace_region[i, j] != trace_region[i, j + 1] and
                        marker[i, j + 1] != -1):

                    numcells += 1
                    boundary = []

                    s = [i, j + 1]
                    prev = [i, j]
                    current_px = s[0]
                    current_py = s[1]

                    boundary.append([current_px, current_py])
                    marker[current_px, current_py] = -1

                    current_px, current_py, prev = get_theo_neighbourhood(
                        trace_region, current_px, current_py, prev
                    )
                    boundary.append([current_px, current_py])
                    marker[current_px, current_py] = -1

                    # Fixed iteration count (matching MATLAB's n < 12000)
                    for _ in range(12000):
                        current_px, current_py, prev = get_theo_neighbourhood(
                            trace_region, current_px, current_py, prev
                        )
                        boundary.append([current_px, current_py])
                        marker[current_px, current_py] = -1

                    B.append(np.array(boundary))

    return B, L
