"""
getCols.m -> get_cols.py

Finds all columns of connected dominos and computes their sums.

Column orientation codes:
    1 = Vertical
    2 = Top Horizontal
    3 = Bottom Horizontal
    4 = Middle Horizontal
"""

import numpy as np
from .top_dom import top_dom
from .bottom_dom import bottom_dom


def get_cols(dominos, adjacent_doms):
    """
    Find all columns with more than one domino and compute their sums.

    Parameters
    ----------
    dominos : np.ndarray
        (num_dominos, 7) array.
    adjacent_doms : np.ndarray
        (num_dominos, num_dominos) relation matrix (will be modified in-place).

    Returns
    -------
    cols : list of np.ndarray
        Each element is a (2, n) array: row 0 = domino indices, row 1 = orientations.
    sums : np.ndarray
        Sum of dot values for each column.
    col_ends : np.ndarray
        (num_cols, 2) array with [first_end_value, last_end_value].
    """
    num_dominos = dominos.shape[0]
    cols = []

    for i in range(num_dominos):
        curr_dom = i
        top = i
        orient = -1
        next_orient = -1

        # Move up until we reach the top of the column
        while top >= 0:
            curr_dom = top
            orient = next_orient
            this_dom = dominos[top]

            if this_dom[4] == 0:  # Vertical
                top, next_orient = top_dom(dominos, adjacent_doms, curr_dom, orient)
            else:  # Horizontal
                top, next_orient = top_dom(dominos, adjacent_doms, curr_dom, 2)
                if top < 0:
                    top, next_orient = top_dom(dominos, adjacent_doms, curr_dom, 3)
                if top < 0:
                    top, next_orient = top_dom(dominos, adjacent_doms, curr_dom, 4)

        # Move down until we reach the bottom of the column
        this_col_doms = [curr_dom]
        this_col_orients = []

        if orient != -1:
            this_col_orients.append(orient)
            bottom, next_orient = bottom_dom(dominos, adjacent_doms, curr_dom, orient)
        else:
            bottom, next_orient = bottom_dom(dominos, adjacent_doms, curr_dom, 1)
            this_col_orients.append(1)

            if bottom < 0:
                bottom, next_orient = bottom_dom(dominos, adjacent_doms, curr_dom, 2)
                this_col_orients[-1] = 2

            if bottom < 0:
                bottom, next_orient = bottom_dom(dominos, adjacent_doms, curr_dom, 3)
                this_col_orients[-1] = 3

            if bottom < 0:
                bottom, next_orient = bottom_dom(dominos, adjacent_doms, curr_dom, 4)
                this_col_orients[-1] = 4

        # Multi-domino column
        if bottom >= 0:
            while bottom >= 0:
                adjacent_doms[curr_dom, bottom] = 0
                adjacent_doms[bottom, curr_dom] = 0

                curr_dom = bottom
                orient = next_orient

                this_col_doms.append(curr_dom)
                this_col_orients.append(orient)

                bottom, next_orient = bottom_dom(dominos, adjacent_doms, curr_dom, orient)

            new_col = np.zeros((2, len(this_col_doms)), dtype=np.int32)
            for j in range(len(this_col_doms)):
                new_col[0, j] = this_col_doms[j]
                new_col[1, j] = this_col_orients[j]

            cols.append(new_col)

    num_cols = len(cols)
    sums = np.zeros(num_cols, dtype=np.int32)
    col_ends = np.zeros((num_cols, 2), dtype=np.int32)

    for i in range(num_cols):
        curr_col = cols[i]
        num_doms = curr_col.shape[1]
        col_sum = 0

        for j in range(num_doms):
            curr_d = dominos[curr_col[0, j]]
            curr_orient = curr_col[1, j]

            if curr_orient == 1:
                col_val = curr_d[5] + curr_d[6]
                start_val = curr_d[5]
                end_val = curr_d[6]
            elif curr_orient == 2:
                col_val = curr_d[5]
                start_val = curr_d[5]
                end_val = curr_d[5]
            elif curr_orient == 3:
                col_val = curr_d[6]
                start_val = curr_d[6]
                end_val = curr_d[6]
            else:  # orient == 4
                col_val = curr_d[5] + curr_d[6]
                start_val = curr_d[5]
                end_val = curr_d[5]

            col_sum += col_val

            if j == 0:
                col_ends[i, 0] = start_val
            if j == num_doms - 1:
                col_ends[i, 1] = end_val

        sums[i] = col_sum

    return cols, sums, col_ends
