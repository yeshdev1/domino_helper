"""
main.m -> main.py

Main entry point for the Domino Helper application.
Loads a domino game image, preprocesses it, detects dominos,
computes row/column sums, and displays the annotated result.
"""

import os
import sys
import cv2
from .game_region import game_region
from .domino_finder import domino_finder


# Available test images
IMAGES = {
    1: 'IMG_0660.JPG',
    2: 'IMG_4421.JPG',
    3: 'IMG_4759.JPG',
    4: 'IMG_7010.JPG',
    5: 'IMG_4384.JPG',
    6: 'IMG_6365.PNG',
    7: 'slantedRight.jpg',
    8: 'slantedRight.jpg',
    9: 'manyRows.jpg',
}


def main(selector=4, image_path=None):
    """
    Run the Domino Helper pipeline.

    Parameters
    ----------
    selector : int
        Index (1-9) to select a built-in test image from the data/ directory.
    image_path : str, optional
        Path to a custom image. Overrides selector if provided.
    """
    if image_path is not None:
        img_path = image_path
    else:
        # Resolve data directory relative to project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', '..', 'data')

        if selector not in IMAGES:
            print(f"Invalid selector {selector}. Choose 1-9.")
            sys.exit(1)

        img_path = os.path.join(data_dir, IMAGES[selector])

    print(f"Loading image: {img_path}")
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error: Could not load image at {img_path}")
        sys.exit(1)

    print("Preprocessing image...")
    region = game_region(img)

    print("Detecting dominos...")
    dominos, annotated, *_ = domino_finder(region, img)

    # Display results
    # Resize for display if image is large
    h, w = annotated.shape[:2]
    max_dim = 1200
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        display_img = cv2.resize(annotated, (int(w * scale), int(h * scale)))
    else:
        display_img = annotated

    cv2.imshow('Domino Helper', display_img)
    print("\nPress any key to close the window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return dominos


if __name__ == '__main__':
    sel = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    img_path = sys.argv[2] if len(sys.argv) > 2 else None
    main(selector=sel, image_path=img_path)
