"""
mooreTracing.m -> moore_tracing.py

Custom Moore neighborhood boundary tracing algorithm.
Scans the binary image for white-to-black transitions and traces each
boundary contour using the getNeighbourhood function.
"""

import numpy as np
from .get_neighbourhood import get_neighbourhood


def moore_tracing(region):
    """
    Trace boundaries in a binary image using Moore neighborhood tracing.

    Parameters
    ----------
    region : np.ndarray
        Binary image (values 0 and 1).

    Returns
    -------
    B : list of np.ndarray
        List of boundary arrays, each of shape (N, 2) with [row, col] coordinates.
    L : list
        Placeholder (matches MATLAB signature).
    """
    B = []
    L = []

    trace_region = region.copy()
    x, y = region.shape
    marker = np.zeros((x, y), dtype=np.int32)

    for i in range(x):
        for j in range(y):
            if j + 1 < y and i + 1 < x:
                # White to black detection
                if (trace_region[i, j + 1] == 0 and
                        trace_region[i, j] != trace_region[i, j + 1] and
                        marker[i, j + 1] != -1):

                    boundary = []

                    s = [i, j + 1]
                    prev = [i, j]
                    current_px = s[0]
                    current_py = s[1]

                    boundary.append([current_px, current_py])
                    marker[current_px, current_py] = -1

                    current_px, current_py, prev = get_neighbourhood(
                        trace_region, current_px, current_py, prev
                    )
                    boundary.append([current_px, current_py])
                    marker[current_px, current_py] = -1

                    while current_px != s[0] or current_py != s[1]:
                        current_px, current_py, prev = get_neighbourhood(
                            trace_region, current_px, current_py, prev
                        )
                        boundary.append([current_px, current_py])
                        marker[current_px, current_py] = -1

                    B.append(np.array(boundary))

    return B, L
