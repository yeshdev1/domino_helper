"""
rightDom.m -> right_dom.py

Returns the domino to the right of the current domino in a row.
"""

import numpy as np


def right_dom(dominos, adjacencies, curr_dom, row_orient):
    """
    Find the domino to the right of curr_dom in the row.

    Parameters
    ----------
    dominos : np.ndarray
        (num_dominos, 7) array.
    adjacencies : np.ndarray
        (num_dominos, num_dominos) relation matrix.
    curr_dom : int
        Index of the current domino (0-based).
    row_orient : int
        Orientation of curr_dom within the row.

    Returns
    -------
    domino : int
        Index of right neighbor (0-based), or -1 if none found.
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

            if this_dom[4] == 1:  # Horizontal
                if other_dom[4] == 1:  # other Horizontal
                    if rel_type == 1:
                        return i, 1
                else:  # other Vertical
                    if rel_type == 1:
                        return i, 3
                    if rel_type == 2:
                        return i, 2
                    if rel_type == 3:
                        return i, 4

            else:  # Vertical
                if row_orient == 2:  # top row
                    if other_dom[4] == 1:
                        if rel_type == 1:
                            return i, 1
                    else:
                        if rel_type == 3:
                            return i, 3

                if row_orient == 3:  # bottom row
                    if other_dom[4] == 1:
                        if rel_type == 2:
                            return i, 1
                    else:
                        if rel_type == 5:
                            return i, 2

                if row_orient == 4:  # middle row
                    if other_dom[4] == 1:
                        if rel_type == 3:
                            return i, 1

    return domino, orientation
