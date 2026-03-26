"""
dominoFinder.m -> domino_finder.py

Core function that detects dominos from the binary region image.
Uses Moore boundary tracing to find contours, identifies circles (dots) and
center lines, extracts domino bounding boxes, counts dots per half,
determines adjacencies, and computes row/column sums.
"""

import numpy as np
import cv2
from .moore_tracing import moore_tracing
from .adj_helper import adj_helper
from .get_rows import get_rows
from .get_cols import get_cols
from .row_sum_loc import row_sum_loc
from .col_sum_loc import col_sum_loc


def domino_finder(region, img):
    """
    Detect dominos, count their dots, find adjacencies, and compute row/col sums.

    Parameters
    ----------
    region : np.ndarray
        Binary image (values 0 and 1).
    img : np.ndarray
        Original BGR color image.

    Returns
    -------
    dominos : np.ndarray
        (num_dominos, 7) array:
        [top, bottom, left, right, vert(0)/hor(1), top/left_dots, bottom/right_dots]
    """
    B, L = moore_tracing(region)

    height, width = img.shape[:2]

    # Find the number of circles and the most common circumference
    num_cells = len(B)
    circles = 0
    most_common_circ = 0

    for i in range(num_cells):
        cell_circ = len(B[i])
        similar_cells = 0

        for j in range(num_cells):
            other_circ = len(B[j])
            if abs(cell_circ - other_circ) < 50:
                similar_cells += 1

        if similar_cells > circles:
            circles = similar_cells
            most_common_circ = cell_circ

    # Find average circle size
    sum_of_circs = 0
    for i in range(num_cells):
        circ = len(B[i])
        if abs(most_common_circ - circ) < 50:
            sum_of_circs += circ

    average_circle_size = sum_of_circs / circles if circles > 0 else 0

    # Find center lines based off circle size
    center_line_estimate = 3 * average_circle_size

    # Separate center lines from other boundaries
    delete_these = []
    for i in range(num_cells):
        circ = len(B[i])
        if abs(center_line_estimate - circ) > 80:
            delete_these.append(i)

    center_lines = [B[i] for i in range(num_cells) if i not in delete_these]

    num_dominos = len(center_lines)
    dominos = np.zeros((num_dominos, 7))

    # Extract dominos from center lines
    # [top, bottom, left, right, vert(0)/hor(1), top/left_dots, bottom/right_dots]

    for i in range(num_dominos):
        top = height
        bottom = 0
        left = width
        right = 0

        for j in range(len(center_lines[i])):
            row_val = center_lines[i][j, 0]
            col_val = center_lines[i][j, 1]

            if row_val < top:
                top = row_val
            if row_val > bottom:
                bottom = row_val
            if col_val < left:
                left = col_val
            if col_val > right:
                right = col_val

        dominos[i, 0] = top
        dominos[i, 1] = bottom
        dominos[i, 2] = left
        dominos[i, 3] = right

        # Horizontal or vertical
        line_length = 0
        if abs(left - right) < abs(top - bottom):
            dominos[i, 4] = 1  # Horizontal (center line is vertical = domino is horizontal)
            line_length = abs(top - bottom)
        else:
            line_length = abs(left - right)

        # Get domino dot values
        top_left_dots = 0
        bottom_right_dots = 0

        if dominos[i, 4] == 0:  # Vertical domino
            for j in range(num_cells):
                circ = len(B[j])
                if abs(average_circle_size - circ) < 50:
                    x_val = B[j][0, 1]  # col
                    y_val = B[j][0, 0]  # row

                    e = 0.1 * line_length

                    left_lim = left - e
                    right_lim = right + e
                    top_lim = top - 1.15 * line_length
                    bottom_lim = bottom + 1.15 * line_length

                    if y_val < top + e and y_val > top_lim and x_val > left_lim and x_val < right_lim:
                        top_left_dots += 1

                    if y_val > bottom - e and y_val < bottom_lim and x_val > left_lim and x_val < right_lim:
                        bottom_right_dots += 1

        else:  # Horizontal domino
            for j in range(num_cells):
                circ = len(B[j])
                if abs(average_circle_size - circ) < 50:
                    x_val = B[j][0, 1]  # col
                    y_val = B[j][0, 0]  # row

                    e = 0.1 * line_length

                    top_lim = top - e
                    bottom_lim = bottom + e
                    left_lim = left - 1.1 * line_length
                    right_lim = right + 1.1 * line_length

                    if x_val < left + e and x_val > left_lim and y_val > top_lim and y_val < bottom_lim:
                        top_left_dots += 1

                    if x_val > right - e and x_val < right_lim and y_val > top_lim and y_val < bottom_lim:
                        bottom_right_dots += 1

        dominos[i, 5] = top_left_dots
        dominos[i, 6] = bottom_right_dots

    # Classify domino adjacencies
    relations = adj_helper(dominos, line_length)
    adjacent_doms = relations.copy()

    # Get rows
    rows, row_sums, row_ends = get_rows(dominos, adjacent_doms.copy())

    # Get columns
    cols, col_sums, col_ends = get_cols(dominos, adjacent_doms.copy())

    num_rows = len(row_sums)
    num_cols = len(col_sums)

    text_positions = np.zeros((num_rows + num_cols, 2))
    text_values = []

    for i in range(num_rows):
        text_values.append(str(int(row_sums[i])))
        x_loc, y_loc = row_sum_loc(dominos, rows[i], line_length)
        text_positions[i, 0] = x_loc
        text_positions[i, 1] = y_loc

    for i in range(num_cols):
        text_values.append(str(int(col_sums[i])))
        x_loc, y_loc = col_sum_loc(dominos, cols[i], line_length)
        text_positions[num_rows + i, 0] = x_loc
        text_positions[num_rows + i, 1] = y_loc

    # Print results
    print(f"\nDetected {num_dominos} dominos")
    print(f"Found {num_rows} rows and {num_cols} columns\n")

    for i in range(num_rows):
        print(f"Row {i + 1} sum: {row_sums[i]}")
    for i in range(num_cols):
        print(f"Col {i + 1} sum: {col_sums[i]}")

    # Annotate image with sums
    annotated = img.copy()
    for i in range(len(text_values)):
        x = int(text_positions[i, 0])
        y = int(text_positions[i, 1])
        cv2.putText(
            annotated, text_values[i], (x, y),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4,
            lineType=cv2.LINE_AA
        )

    return dominos, annotated
