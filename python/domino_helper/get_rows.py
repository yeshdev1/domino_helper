"""
getRows.m -> get_rows.py

Finds all rows of connected dominos and computes their sums.

Row orientation codes:
    1 = horizontal
    2 = Top Vertical
    3 = Bottom Vertical
    4 = Middle Vertical
"""

import numpy as np
from .left_dom import left_dom
from .right_dom import right_dom


def get_rows(dominos, adjacent_doms):
    """
    Find all rows with more than one domino and compute their sums.

    Parameters
    ----------
    dominos : np.ndarray
        (num_dominos, 7) array.
    adjacent_doms : np.ndarray
        (num_dominos, num_dominos) relation matrix (will be modified in-place).

    Returns
    -------
    rows : list of np.ndarray
        Each element is a (2, n) array: row 0 = domino indices, row 1 = orientations.
    sums : np.ndarray
        Sum of dot values for each row.
    row_ends : np.ndarray
        (num_rows, 2) array with [first_end_value, last_end_value].
    """
    num_dominos = dominos.shape[0]
    rows = []

    for i in range(num_dominos):
        curr_dom = i
        left = i
        orient = -1
        next_orient = -1

        # Move left until we reach the beginning of the row
        while left >= 0:
            curr_dom = left
            orient = next_orient
            this_dom = dominos[left]

            if this_dom[4] == 1:  # Horizontal
                left, next_orient = left_dom(dominos, adjacent_doms, curr_dom, orient)
                if left >= 0:
                    curr_dom = left
            else:  # Vertical
                if orient != -1:
                    left, next_orient = left_dom(dominos, adjacent_doms, curr_dom, orient)
                else:
                    left, next_orient = left_dom(dominos, adjacent_doms, curr_dom, 2)
                    if left < 0:
                        left, next_orient = left_dom(dominos, adjacent_doms, curr_dom, 3)
                    if left < 0:
                        left, next_orient = left_dom(dominos, adjacent_doms, curr_dom, 4)

        # Move right until we reach the end of the row
        this_row_doms = [curr_dom]
        this_row_orients = []

        if orient != -1:
            this_row_orients.append(orient)
            right, next_orient = right_dom(dominos, adjacent_doms, curr_dom, orient)
        else:
            right, next_orient = right_dom(dominos, adjacent_doms, curr_dom, 1)
            this_row_orients.append(1)

            if right < 0:
                right, next_orient = right_dom(dominos, adjacent_doms, curr_dom, 2)
                this_row_orients[-1] = 2

            if right < 0:
                right, next_orient = right_dom(dominos, adjacent_doms, curr_dom, 3)
                this_row_orients[-1] = 3

            if right < 0:
                right, next_orient = right_dom(dominos, adjacent_doms, curr_dom, 4)
                this_row_orients[-1] = 4

        # Multi-domino row
        if right >= 0:
            while right >= 0:
                adjacent_doms[curr_dom, right] = 0
                adjacent_doms[right, curr_dom] = 0

                curr_dom = right
                orient = next_orient

                this_row_doms.append(curr_dom)
                this_row_orients.append(orient)

                right, next_orient = right_dom(dominos, adjacent_doms, curr_dom, orient)

            new_row = np.zeros((2, len(this_row_doms)), dtype=np.int32)
            for j in range(len(this_row_doms)):
                new_row[0, j] = this_row_doms[j]
                new_row[1, j] = this_row_orients[j]

            rows.append(new_row)

    num_rows = len(rows)
    sums = np.zeros(num_rows, dtype=np.int32)
    row_ends = np.zeros((num_rows, 2), dtype=np.int32)

    for i in range(num_rows):
        curr_row = rows[i]
        num_doms = curr_row.shape[1]
        row_sum = 0

        for j in range(num_doms):
            curr_d = dominos[curr_row[0, j]]
            curr_orient = curr_row[1, j]

            if curr_orient == 1:
                row_val = curr_d[5] + curr_d[6]
                start_val = curr_d[5]
                end_val = curr_d[6]
            elif curr_orient == 2:
                row_val = curr_d[5]
                start_val = curr_d[5]
                end_val = curr_d[5]
            elif curr_orient == 3:
                row_val = curr_d[6]
                start_val = curr_d[6]
                end_val = curr_d[6]
            else:  # orient == 4
                row_val = curr_d[5] + curr_d[6]
                start_val = curr_d[5]
                end_val = curr_d[5]

            row_sum += row_val

            if j == 0:
                row_ends[i, 0] = start_val
            if j == num_doms - 1:
                row_ends[i, 1] = end_val

        sums[i] = row_sum

    return rows, sums, row_ends
