"""
cornerDetector.m -> corner_detector.py

Alternative domino detection using OpenCV's built-in bwboundaries equivalent.
Counts dominos by boundary circumference and removes noise.
"""

import numpy as np
import cv2


def corner_detector(region):
    """
    Detect domino boundaries and count dots using contour analysis.

    Parameters
    ----------
    region : np.ndarray
        Binary image.

    Returns
    -------
    corners : np.ndarray
        The input region (pass-through, matches MATLAB signature).
    """
    corners = region.copy()

    # Find contours (equivalent to bwboundaries)
    contours, hierarchy = cv2.findContours(
        region.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    # Threshold for domino size
    max_perim = 1500
    for i in range(1, len(contours)):
        perim = len(contours[i])
        if perim > max_perim:
            max_perim = perim

    # Count dominos and identify noise
    num_dominos = 0
    delete_these = []

    for i in range(len(contours)):
        perim = len(contours[i])
        if perim < 100:
            delete_these.append(i)
        if perim > 0.75 * max_perim:
            num_dominos += 1

    num_dominos -= 1  # Discount the border

    # Remove noise contours
    filtered_contours = [
        contours[i] for i in range(len(contours)) if i not in delete_these
    ]

    dot_count = len(filtered_contours) - (num_dominos * 2) - 1

    print(f"Number of dominos: {num_dominos}")
    print(f"Number of dots: {dot_count}")

    return corners
