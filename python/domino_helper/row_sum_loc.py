"""
rowSumLoc.m -> row_sum_loc.py

Computes the (x, y) position to display the row sum text on the image.
"""


def row_sum_loc(dominos, line, line_length):
    """
    Calculate text position for a row sum label.

    Parameters
    ----------
    dominos : np.ndarray
        (num_dominos, 7) array.
    line : np.ndarray
        (2, n) array for this row.
    line_length : float

    Returns
    -------
    x_loc : float
    y_loc : float
    """
    num_doms = line.shape[1]
    last = line[:, num_doms - 1]
    last_dom = dominos[int(last[0])]
    correct = line_length * 0.25

    if last[1] == 1:  # Horizontal
        x_loc = last_dom[3] + 1.5 * line_length
        y_loc = (last_dom[0] + last_dom[1]) / 2 - correct
    else:
        x_loc = last_dom[3] + 0.5 * line_length

        if last[1] == 2:  # Top
            y_loc = last_dom[0] - 0.5 * line_length - correct
        elif last[1] == 3:  # Bottom
            y_loc = last_dom[0] + 0.5 * line_length - correct
        else:  # Middle (4)
            y_loc = last_dom[0] - correct

    return x_loc, y_loc
