"""
rightLook.m -> right_look.py

Looks to the right of the current pixel for the next boundary pixel.
Used by get_theo_neighbourhood.
"""


def right_look(trace_region, current_px, current_py, prev, truth):
    """
    Check 3 pixels to the right for a boundary continuation.

    Returns
    -------
    next_px, next_py, next_prev, new_truth
    """
    next_px = current_px
    next_py = current_py
    next_prev = list(prev)
    new_truth = 0

    current_val = trace_region[current_px, current_py]

    p1 = trace_region[current_px - 1, current_py + 1]
    p2 = trace_region[current_px, current_py + 1]
    p3 = trace_region[current_px + 1, current_py + 1]

    if p1 == current_val:
        return current_px - 1, current_py + 1, [current_px, current_py + 1], 1

    if p2 == current_val:
        return current_px, current_py + 1, [current_px, current_py], 1

    if p3 == current_val:
        return current_px + 1, current_py + 1, [current_px, current_py + 1], 1

    return next_px, next_py, next_prev, new_truth
