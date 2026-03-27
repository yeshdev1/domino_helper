"""
adjHelper.m -> adj_helper.py

Classifies domino adjacencies based on their spatial relationships.
Builds a relation matrix encoding how each pair of dominos is positioned
relative to each other (same row, same column, orientation combos).

Relation codes:
  Two Verticals:   1=SCT, 2=SCB, 3=SRTR, 4=SRTL, 5=SRBR, 6=SRBL
  Two Horizontals: 1=SRR, 2=SRL, 3=SCTR, 4=SCTL, 5=SCBR, 6=SCBL
  Vert & Hor:      1=SRTR, 2=SRBR, 3=SRER, 4=SRTL, 5=SRBL, 6=SREL,
                    7=SCTR, 8=SCTL, 9=SCTE, 10=SCBR, 11=SCBL, 12=SCBE
"""

import numpy as np


def adj_helper(dominos, line_length):
    """
    Build an adjacency/relation matrix for all dominos.

    Parameters
    ----------
    dominos : np.ndarray
        Array of shape (num_dominos, 7) where columns are:
        [top, bottom, left, right, vert(0)/hor(1), top/left_dots, bottom/right_dots]
    line_length : float
        Estimated center line length used for proximity thresholds.

    Returns
    -------
    relations : np.ndarray
        Square matrix of shape (num_dominos, num_dominos) with relation codes.
    """
    num_dominos = dominos.shape[0]
    relations = np.zeros((num_dominos, num_dominos), dtype=np.int32)

    err = 0.25 * line_length
    ll = 1.1 * line_length  # adjusted line_length

    for i in range(num_dominos):
        for j in range(num_dominos):
            d1 = dominos[i]
            d2 = dominos[j]

            if d1[4] == 0:  # i is vertical
                if d2[4] == 0:  # j is vertical
                    # Same Col Top
                    if abs(d1[2] - d2[2]) < err and abs(d1[0] - 2.1 * ll - d2[1]) < err:
                        relations[i, j] = 1
                    # Same Col Bottom
                    if abs(d1[2] - d2[2]) < err and abs(d1[0] + 2.1 * ll - d2[1]) < err:
                        relations[i, j] = 2
                    # Same Row Top Right
                    if abs((d1[0] - ll) - d2[0]) < err and abs((d1[3] + 0.2 * ll) - d2[2]) < err:
                        relations[i, j] = 3
                    # Same Row Top Left
                    if abs((d1[0] - ll) - d2[0]) < err and abs((d1[2] - 0.2 * ll) - d2[3]) < err:
                        relations[i, j] = 4
                    # Same Row Bottom Right
                    if abs((d1[0] + ll) - d2[0]) < err and abs((d1[3] + 0.2 * ll) - d2[2]) < err:
                        relations[i, j] = 5
                    # Same Row Bottom Left
                    if abs((d1[0] + ll) - d2[0]) < err and abs((d1[2] - 0.2 * ll) - d2[3]) < err:
                        relations[i, j] = 6

                else:  # j is horizontal
                    # Same Row Top Right
                    if abs(d1[0] - d2[1]) < err and abs((d1[3] + ll) - d2[2]) < err:
                        relations[i, j] = 1
                    # Same Row Bottom Right
                    if abs(d1[1] - d2[0]) < err and abs((d1[3] + ll) - d2[2]) < err:
                        relations[i, j] = 2
                    # Same Row Even Right
                    if abs((d1[0] - 0.5 * ll) - d2[0]) < err and abs((d1[3] + ll) - d2[2]) < err:
                        relations[i, j] = 3
                    # Same Row Top Left
                    if abs(d1[0] - d2[1]) < err and abs((d1[2] - ll) - d2[3]) < err:
                        relations[i, j] = 4
                    # Same Row Bottom Left
                    if abs(d1[1] - d2[0]) < err and abs((d1[2] - ll) - d2[3]) < err:
                        relations[i, j] = 5
                    # Same Row Even Left
                    if abs((d1[0] - 0.5 * ll) - d2[0]) < err and abs((d1[2] - ll) - d2[3]) < err:
                        relations[i, j] = 6
                    # Same Col Top Right
                    if abs(d1[3] - d2[2]) < err and abs((d1[0] - ll) - d2[1]) < err:
                        relations[i, j] = 7
                    # Same Col Top Left
                    if abs(d1[2] - d2[3]) < err and abs((d1[0] - ll) - d2[1]) < err:
                        relations[i, j] = 8
                    # Same Col Top Even
                    if abs((d1[3] - 0.5 * ll) - d2[3]) < err and abs((d1[0] - ll) - d2[1]) < err:
                        relations[i, j] = 9
                    # Same Col Bottom Right
                    if abs(d1[3] - d2[2]) < err and abs((d1[1] + ll) - d2[0]) < err:
                        relations[i, j] = 10
                    # Same Col Bottom Left
                    if abs(d1[2] - d2[3]) < err and abs((d1[1] + ll) - d2[0]) < err:
                        relations[i, j] = 11
                    # Same Col Bottom Even
                    if abs((d1[3] - 0.5 * ll) - d2[3]) < err and abs((d1[1] + ll) - d2[0]) < err:
                        relations[i, j] = 12

            else:  # i is horizontal
                if d2[4] == 1:  # j is horizontal
                    # Same Row Right
                    if abs(d1[0] - d2[0]) < err and abs(d1[3] + 2 * ll - d2[2]) < err:
                        relations[i, j] = 1
                    # Same Row Left
                    if abs(d1[0] - d2[0]) < err and abs(d1[2] - 2 * ll - d2[3]) < err:
                        relations[i, j] = 2
                    # Same Col Top Right
                    if abs((d1[3] + ll) - d2[2]) < err and abs((d1[0] - 0.2 * ll) - d2[1]) < err:
                        relations[i, j] = 3
                    # Same Col Top Left
                    if abs((d1[2] - ll) - d2[3]) < err and abs((d1[0] - 0.2 * ll) - d2[1]) < err:
                        relations[i, j] = 4
                    # Same Col Bottom Right
                    if abs((d1[3] + ll) - d2[2]) < err and abs((d1[1] + 0.2 * ll) - d2[0]) < err:
                        relations[i, j] = 5
                    # Same Col Bottom Left
                    if abs((d1[2] - ll) - d2[3]) < err and abs((d1[1] + 0.2 * ll) - d2[0]) < err:
                        relations[i, j] = 6

                else:  # j is vertical
                    # Same Row Top Right
                    if abs(d1[0] - d2[1]) < err and abs((d1[3] + ll) - d2[2]) < err:
                        relations[i, j] = 1
                    # Same Row Bottom Right
                    if abs(d1[1] - d2[0]) < err and abs((d1[3] + ll) - d2[2]) < err:
                        relations[i, j] = 2
                    # Same Row Even Right
                    if abs((d1[0] - 0.5 * ll) - d2[0]) < err and abs((d1[3] + ll) - d2[2]) < err:
                        relations[i, j] = 3
                    # Same Row Top Left
                    if abs(d1[0] - d2[1]) < err and abs((d1[2] - ll) - d2[3]) < err:
                        relations[i, j] = 4
                    # Same Row Bottom Left
                    if abs(d1[1] - d2[0]) < err and abs((d1[2] - ll) - d2[3]) < err:
                        relations[i, j] = 5
                    # Same Row Even Left
                    if abs((d1[0] - 0.5 * ll) - d2[0]) < err and abs((d1[2] - ll) - d2[3]) < err:
                        relations[i, j] = 6
                    # Same Col Top Right
                    if abs(d1[3] - d2[2]) < err and abs((d1[0] - ll) - d2[1]) < err:
                        relations[i, j] = 7
                    # Same Col Top Left
                    if abs(d1[2] - d2[3]) < err and abs((d1[0] - ll) - d2[1]) < err:
                        relations[i, j] = 8
                    # Same Col Top Even
                    if abs((d1[2] - 0.4 * ll) - d2[2]) < err and abs((d1[0] - ll) - d2[1]) < err:
                        relations[i, j] = 9
                    # Same Col Bottom Right
                    if abs(d1[3] - d2[2]) < err and abs((d1[1] + ll) - d2[0]) < err:
                        relations[i, j] = 10
                    # Same Col Bottom Left
                    if abs(d1[2] - d2[3]) < err and abs((d1[1] + ll) - d2[0]) < err:
                        relations[i, j] = 11
                    # Same Col Bottom Even
                    if abs((d1[2] - 0.4 * ll) - d2[2]) < err and abs((d1[1] + ll) - d2[0]) < err:
                        relations[i, j] = 12

    return relations
