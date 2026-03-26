"""
bottomDom.m -> bottom_dom.py

Returns the domino below the current domino in a column.
"""

import numpy as np


def bottom_dom(dominos, adjacencies, curr_dom, row_orient):
    """
    Find the domino below curr_dom in the column.

    Parameters
    ----------
    dominos : np.ndarray
        (num_dominos, 7) array.
    adjacencies : np.ndarray
        (num_dominos, num_dominos) relation matrix.
    curr_dom : int
        Index of the current domino (0-based).
    row_orient : int
        Orientation of curr_dom within the column.

    Returns
    -------
    domino : int
        Index of bottom neighbor (0-based), or -1 if none found.
    orientation : int
    """
    num_dominos = len(adjacencies)
    this_dom = dominos[curr_dom]
    domino = -1
    orientation = 0

    for i in range(num_dominos):
        other_dom = dominos[i]
        if adjacencies[curr_dom, i] != 0:
            rel_type = adjacencies[curr_dom, i]

            if this_dom[4] == 0:  # Vertical
                if other_dom[4] == 0:  # other Vertical
                    if rel_type == 2:
                        return i, 1
                else:  # other Horizontal
                    if rel_type == 10:
                        return i, 2
                    if rel_type == 11:
                        return i, 3
                    if rel_type == 12:
                        return i, 4

            else:  # Horizontal
                if row_orient == 3:  # right col
                    if other_dom[4] == 0:
                        if rel_type == 10:
                            return i, 1
                    else:
                        if rel_type == 5:
                            return i, 3

                if row_orient == 2:  # left col
                    if other_dom[4] == 0:
                        if rel_type == 11:
                            return i, 1
                    else:
                        if rel_type == 6:
                            return i, 2

                if row_orient == 4:  # middle col
                    if other_dom[4] == 0:
                        if rel_type == 12:
                            return i, 1

    return domino, orientation
