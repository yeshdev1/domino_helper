"""
gameRegion.m -> game_region.py

Preprocesses the game image: applies an averaging filter, converts to grayscale,
applies Otsu's threshold, and inverts the binary image to isolate domino regions.
"""

import numpy as np
import cv2


def game_region(img):
    """
    Convert a color image of a domino game into a binary region image.

    Parameters
    ----------
    img : np.ndarray
        BGR color image (as read by cv2.imread).

    Returns
    -------
    region : np.ndarray
        Binary image (uint8, values 0 or 1) where 1 = foreground (domino features).
    """
    # Average filter 15x15
    kernel = np.ones((15, 15), np.float64) / (15 * 15)
    img_filtered = cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REPLICATE)

    # Convert to grayscale
    gray = cv2.cvtColor(img_filtered, cv2.COLOR_BGR2GRAY)

    # Otsu's threshold (equivalent to graythresh + im2bw)
    _, bw = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert (~ BW in MATLAB)
    region = 1 - bw

    return region
