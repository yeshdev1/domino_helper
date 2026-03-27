"""
colSumLoc.m -> col_sum_loc.py

Computes the (x, y) position to display the column sum text on the image.
"""


def col_sum_loc(dominos, line, line_length):
    """
    Calculate text position for a column sum label.

    Parameters
    ----------
    dominos : np.ndarray
        (num_dominos, 7) array.
    line : np.ndarray
        (2, n) array for this column.
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

    if last[1] == 1:  # Vertical
        y_loc = last_dom[1] + 1.5 * line_length
        x_loc = (last_dom[2] + last_dom[3]) / 2 - correct
    else:
        y_loc = last_dom[1] + 0.5 * line_length

        if last[1] == 2:  # Left
            x_loc = last_dom[2] - 0.5 * line_length - correct
        elif last[1] == 3:  # Right
            x_loc = last_dom[3] + 0.5 * line_length - correct
        else:  # Middle (4)
            x_loc = last_dom[2] - correct

    return x_loc, y_loc
