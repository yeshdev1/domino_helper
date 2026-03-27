"""
game_region.py — Modernized image preprocessing.

Replaces the original 15x15 average filter + global Otsu threshold with:
  - Gaussian blur (better edge preservation than box filter)
  - Adaptive Gaussian thresholding (handles uneven lighting)
  - Morphological cleanup (closes small gaps in center lines)
"""

import numpy as np
import cv2


def game_region(img, block_size=51, C=10, morph_kernel_size=3):
    """
    Convert a color image of a domino game into a clean binary region image.

    Parameters
    ----------
    img : np.ndarray
        BGR color image (as read by cv2.imread).
    block_size : int
        Block size for adaptive thresholding (must be odd). Larger values
        handle more gradual lighting changes. Default 51.
    C : int
        Constant subtracted from the adaptive threshold mean. Higher values
        make thresholding more aggressive (fewer white pixels). Default 10.
    morph_kernel_size : int
        Size of the morphological structuring element for cleanup. Default 3.

    Returns
    -------
    region : np.ndarray
        Binary image (uint8, values 0 or 255) where 255 = foreground.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Light Gaussian blur to reduce noise without destroying dot edges
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Gaussian threshold — handles uneven lighting across the board
    # much better than global Otsu, which fails when one side is brighter
    bw = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, block_size, C
    )

    # Invert so domino features (dots, lines) are white (255)
    region = cv2.bitwise_not(bw)

    # Morphological close to bridge small gaps in center lines,
    # then open to remove isolated noise pixels
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (morph_kernel_size, morph_kernel_size)
    )
    region = cv2.morphologyEx(region, cv2.MORPH_CLOSE, kernel, iterations=1)
    region = cv2.morphologyEx(region, cv2.MORPH_OPEN, kernel, iterations=1)

    return region
