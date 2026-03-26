"""
getNeighbourhood.m -> get_neighbourhood.py

Given the current pixel on a boundary and the previous pixel, determines the
next boundary pixel by checking neighbors in a Moore neighborhood pattern.
Four directional cases based on where the previous pixel is relative to current.
"""

import numpy as np


def _check(trace_region, r, c, prev_r, prev_c):
    """Return True if pixel at (r, c) differs from pixel at (prev_r, prev_c)."""
    return trace_region[r, c] != trace_region[prev_r, prev_c]


def get_neighbourhood(trace_region, current_px, current_py, prev):
    """
    Find the next boundary pixel using Moore neighborhood tracing.

    Parameters
    ----------
    trace_region : np.ndarray
        Binary image.
    current_px : int
        Current pixel row.
    current_py : int
        Current pixel column.
    prev : list
        [row, col] of previous pixel.

    Returns
    -------
    next_px : int
    next_py : int
    next_prev : list
    """
    prev_val_r, prev_val_c = prev[0], prev[1]
    next_px = current_px
    next_py = current_py
    next_prev = list(prev)

    # Case 1: prev is to the LEFT of current (prev_col < current_col, same row)
    if prev[1] < current_py and prev[0] == current_px:
        cp = [prev[0], prev[1]]

        # 1: up
        cp[0] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], list(prev)

        # 2: up-right
        cp[1] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] - 1]

        # 3: right
        cp[1] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] - 1]

        # 4: down-right
        cp[0] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] - 1, cp[1]]

        # 5: down
        cp[0] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] - 1, cp[1]]

        # 6: down-left
        cp[1] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] + 1]

        # 7: left
        cp[1] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] + 1]

        # 8: up-left
        cp[0] -= 1
        return next_px, next_py, next_prev

    # Case 2: prev is to the RIGHT of current (prev_col > current_col, same row)
    elif prev[1] > current_py and prev[0] == current_px:
        cp = [prev[0], prev[1]]

        # 1: down
        cp[0] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], list(prev)

        # 2: down-left
        cp[1] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] + 1]

        # 3: left
        cp[1] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] + 1]

        # 4: up-left
        cp[0] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] + 1, cp[1]]

        # 5: up
        cp[0] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] + 1, cp[1]]

        # 6: up-right
        cp[1] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] - 1]

        # 7: right
        cp[1] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] - 1]

        # 8: down-right
        cp[0] += 1
        return next_px, next_py, next_prev

    # Case 3: prev is ABOVE current (prev_row < current_row, same col)
    elif prev[0] < current_px and prev[1] == current_py:
        cp = [prev[0], prev[1]]

        # 1: right
        cp[1] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], list(prev)

        # 2: down-right
        cp[0] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] - 1, cp[1]]

        # 3: down
        cp[0] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] - 1, cp[1]]

        # 4: down-left
        cp[1] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] + 1]

        # 5: left
        cp[1] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] + 1]

        # 6: up-left
        cp[0] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] + 1, cp[1]]

        # 7: up
        cp[0] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] + 1, cp[1]]

        # 8: up-right
        cp[1] += 1
        return next_px, next_py, next_prev

    # Case 4: prev is BELOW current (prev_row > current_row, same col)
    elif prev[0] > current_px and prev[1] == current_py:
        cp = [prev[0], prev[1]]

        # 1: left
        cp[1] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], list(prev)

        # 2: up-left
        cp[0] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] + 1, cp[1]]

        # 3: up
        cp[0] -= 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] + 1, cp[1]]

        # 4: up-right
        cp[1] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] - 1]

        # 5: right
        cp[1] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0], cp[1] - 1]

        # 6: down-right
        cp[0] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] - 1, cp[1]]

        # 7: down
        cp[0] += 1
        if _check(trace_region, cp[0], cp[1], prev_val_r, prev_val_c):
            return cp[0], cp[1], [cp[0] - 1, cp[1]]

        # 8: down-left
        cp[1] -= 1
        return next_px, next_py, next_prev

    return next_px, next_py, next_prev
