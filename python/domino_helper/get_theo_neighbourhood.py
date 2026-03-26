"""
getTheoNeighbourhood.m -> get_theo_neighbourhood.py

Alternative neighbourhood lookup that delegates to directional look functions
(left_lookup, right_look, up_look, down_look). Used by theo_tracing.
"""

from .left_lookup import left_lookup
from .right_look import right_look
from .up_look import up_look
from .down_look import down_look


def get_theo_neighbourhood(trace_region, current_px, current_py, prev):
    """
    Find the next boundary pixel using directional look functions.

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
    next_px, next_py, next_prev
    """
    truth = 0
    next_px = current_px
    next_py = current_py
    next_prev = list(prev)

    # prev is to the LEFT (same row, prev col < current col)
    if prev[0] == current_px and prev[1] < current_py:
        next_px, next_py, next_prev, truth = right_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = down_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = left_lookup(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = up_look(
            trace_region, current_px, current_py, prev, truth
        )
        return next_px, next_py, next_prev

    # prev is to the RIGHT (same row, prev col > current col)
    elif prev[0] == current_px and prev[1] > current_py:
        next_px, next_py, next_prev, truth = left_lookup(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = up_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = right_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = down_look(
            trace_region, current_px, current_py, prev, truth
        )
        return next_px, next_py, next_prev

    # prev is BELOW (prev row > current row, same col)
    elif prev[0] > current_px and prev[1] == current_py:
        next_px, next_py, next_prev, truth = up_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = right_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = down_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = left_lookup(
            trace_region, current_px, current_py, prev, truth
        )
        return next_px, next_py, next_prev

    # prev is ABOVE (prev row < current row, same col)
    elif prev[0] < current_px and prev[1] == current_py:
        next_px, next_py, next_prev, truth = down_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = left_lookup(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = up_look(
            trace_region, current_px, current_py, prev, truth
        )
        if truth == 1:
            return next_px, next_py, next_prev

        next_px, next_py, next_prev, truth = right_look(
            trace_region, current_px, current_py, prev, truth
        )
        return next_px, next_py, next_prev

    return next_px, next_py, next_prev
