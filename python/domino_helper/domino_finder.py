"""
domino_finder.py — Modernized domino detection pipeline.

Replaces custom Moore boundary tracing with OpenCV's C-optimized findContours.
Uses area + circularity for contour classification (resolution-independent)
instead of brittle circumference matching. Computes dot centroids via cv2.moments
for more robust half-assignment.

Output contract unchanged: returns (num_dominos, 7) array with
[top, bottom, left, right, vert(0)/hor(1), top_left_dots, bottom_right_dots]
"""

import numpy as np
import cv2
from .adj_helper import adj_helper
from .get_rows import get_rows
from .get_cols import get_cols
from .row_sum_loc import row_sum_loc
from .col_sum_loc import col_sum_loc


def _classify_contours(contours, hierarchy):
    """
    Classify contours into dots, center lines, and noise using area and
    circularity (4*pi*area / perimeter^2). Resolution-independent via ratios.

    Returns
    -------
    dot_indices : list of int
    center_line_indices : list of int
    areas : np.ndarray
    circularities : np.ndarray
    centroids : list of (cx, cy) tuples
    """
    n = len(contours)
    areas = np.zeros(n)
    perimeters = np.zeros(n)
    circularities = np.zeros(n)
    centroids = [(0.0, 0.0)] * n

    for i in range(n):
        areas[i] = cv2.contourArea(contours[i])
        perimeters[i] = cv2.arcLength(contours[i], closed=True)
        if perimeters[i] > 0:
            circularities[i] = 4 * np.pi * areas[i] / (perimeters[i] ** 2)
        M = cv2.moments(contours[i])
        if M['m00'] > 0:
            centroids[i] = (M['m10'] / M['m00'], M['m01'] / M['m00'])

    # Filter out noise (very small contours)
    min_area = np.median(areas[areas > 0]) * 0.1 if np.any(areas > 0) else 10
    valid = areas > min_area

    # Among valid contours, find the dominant area cluster (dots are most numerous)
    valid_areas = areas[valid]
    if len(valid_areas) == 0:
        return [], [], areas, circularities, centroids

    # Use the most common area range to identify dots
    # Sort areas and find the largest cluster of similar-sized contours
    sorted_areas = np.sort(valid_areas)
    best_count = 0
    best_median = sorted_areas[0]

    for a in sorted_areas:
        # Count how many contours have area within 50% of this one
        similar = np.sum(np.abs(valid_areas - a) < a * 0.5)
        if similar > best_count:
            best_count = similar
            best_median = a

    # Dot area threshold: within 50% of the dominant size
    dot_lo = best_median * 0.5
    dot_hi = best_median * 1.5

    # Center line area estimate: ~9x dot area (perimeter ~3x means area ~9x)
    # but allow a wide range since center lines vary in thickness
    cl_estimate = best_median * 9
    cl_lo = cl_estimate * 0.3
    cl_hi = cl_estimate * 3.0

    dot_indices = []
    center_line_indices = []

    for i in range(n):
        if not valid[i]:
            continue

        # Skip outermost contour (image border) if present
        if hierarchy is not None and hierarchy[0, i, 3] == -1 and areas[i] > cl_hi * 2:
            continue

        a = areas[i]
        c = circularities[i]

        if dot_lo <= a <= dot_hi and c > 0.45:
            dot_indices.append(i)
        elif cl_lo <= a <= cl_hi and c < 0.55:
            center_line_indices.append(i)

    return dot_indices, center_line_indices, areas, circularities, centroids


def domino_finder(region, img):
    """
    Detect dominos, count their dots, find adjacencies, and compute row/col sums.

    Parameters
    ----------
    region : np.ndarray
        Binary image (uint8, 0/255) from game_region().
    img : np.ndarray
        Original BGR color image.

    Returns
    -------
    dominos : np.ndarray
        (num_dominos, 7) array:
        [top, bottom, left, right, vert(0)/hor(1), top/left_dots, bottom/right_dots]
    annotated : np.ndarray
        Copy of img with row/col sums overlaid.
    """
    # --- Step 1: Find contours with hierarchy (C-optimized, replaces Moore tracing) ---
    contours, hierarchy = cv2.findContours(
        region, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    if hierarchy is not None:
        hierarchy = hierarchy[0]  # shape (N, 4)
    else:
        hierarchy = np.zeros((0, 4), dtype=np.int32)

    # --- Step 2: Classify contours by area + circularity ---
    dot_indices, cl_indices, areas, circs, centroids = _classify_contours(
        contours, hierarchy.reshape(1, -1, 4) if len(hierarchy) > 0 else None
    )

    # --- Step 3: Extract domino data from center lines ---
    num_dominos = len(cl_indices)
    dominos = np.zeros((num_dominos, 7))
    line_lengths = np.zeros(num_dominos)

    for i, ci in enumerate(cl_indices):
        x, y, w, h = cv2.boundingRect(contours[ci])
        # OpenCV boundingRect: x=col, y=row, w=width, h=height
        top = y
        bottom = y + h
        left = x
        right = x + w

        dominos[i, 0] = top
        dominos[i, 1] = bottom
        dominos[i, 2] = left
        dominos[i, 3] = right

        # Orientation: if center line is taller than wide, domino is horizontal
        if w < h:
            dominos[i, 4] = 1  # horizontal domino
            line_lengths[i] = h
        else:
            line_lengths[i] = w

    # Use median line length as the representative scale factor
    line_length = float(np.median(line_lengths)) if num_dominos > 0 else 0

    # --- Step 4: Count dots per domino half using centroids ---
    # Pre-compute dot centroids (col, row) for vectorized lookup
    dot_centroids = np.array([centroids[di] for di in dot_indices]) if dot_indices else np.empty((0, 2))

    for i in range(num_dominos):
        top = dominos[i, 0]
        bottom = dominos[i, 1]
        left = dominos[i, 2]
        right = dominos[i, 3]
        ll = line_lengths[i]
        top_left_dots = 0
        bottom_right_dots = 0

        if len(dot_centroids) == 0:
            continue

        cx = dot_centroids[:, 0]  # col coordinates
        cy = dot_centroids[:, 1]  # row coordinates

        if dominos[i, 4] == 0:  # Vertical domino
            e = 0.1 * ll
            left_lim = left - e
            right_lim = right + e
            top_lim = top - 1.15 * ll
            bottom_lim = bottom + 1.15 * ll

            # Top half dots
            mask_top = (cy < top + e) & (cy > top_lim) & (cx > left_lim) & (cx < right_lim)
            top_left_dots = int(np.sum(mask_top))

            # Bottom half dots
            mask_bot = (cy > bottom - e) & (cy < bottom_lim) & (cx > left_lim) & (cx < right_lim)
            bottom_right_dots = int(np.sum(mask_bot))

        else:  # Horizontal domino
            e = 0.1 * ll
            top_lim = top - e
            bottom_lim = bottom + e
            left_lim = left - 1.1 * ll
            right_lim = right + 1.1 * ll

            # Left half dots
            mask_left = (cx < left + e) & (cx > left_lim) & (cy > top_lim) & (cy < bottom_lim)
            top_left_dots = int(np.sum(mask_left))

            # Right half dots
            mask_right = (cx > right - e) & (cx < right_lim) & (cy > top_lim) & (cy < bottom_lim)
            bottom_right_dots = int(np.sum(mask_right))

        dominos[i, 5] = top_left_dots
        dominos[i, 6] = bottom_right_dots

    # --- Step 5: Adjacency + row/col analysis (unchanged logic) ---
    relations = adj_helper(dominos, line_length)
    adjacent_doms = relations.copy()

    rows, row_sums, row_ends = get_rows(dominos, adjacent_doms.copy())
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

    return dominos, annotated, rows, row_sums, cols, col_sums
