"""
downLook.m -> down_look.py

Looks below the current pixel for the next boundary pixel.
Used by get_theo_neighbourhood.
"""


def down_look(trace_region, current_px, current_py, prev, truth):
    """
    Check 3 pixels below for a boundary continuation.

    Returns
    -------
    next_px, next_py, next_prev, truth
    """
    next_px = current_px
    next_py = current_py
    next_prev = list(prev)

    current_val = trace_region[current_px, current_py]

    p1 = trace_region[current_px + 1, current_py + 1]
    p2 = trace_region[current_px + 1, current_py]
    p3 = trace_region[current_px + 1, current_py - 1]

    if p1 == current_val:
        return current_px + 1, current_py + 1, [current_px + 1, current_py], 1

    if p2 == current_val:
        return current_px + 1, current_py, [current_px, current_py], 1

    if p3 == current_val:
        return current_px + 1, current_py - 1, [current_px + 1, current_py], 1

    return next_px, next_py, next_prev, truth
