# Domino Helper - Python

A modernized Python implementation of the MATLAB Domino Helper project. Takes a picture of an ongoing dominos game and analyzes the board to detect dominos, count dots, identify rows and columns, and compute sums to help predict the next best move.

## What Changed from the MATLAB Original

| Aspect | MATLAB / Old Python | Modernized Python |
|--------|-------------------|-------------------|
| **Contour detection** | Custom Moore tracing (pure Python pixel loops) | `cv2.findContours` (C-optimized, ~100x faster) |
| **Preprocessing** | 15x15 box filter + global Otsu threshold | Gaussian blur + adaptive threshold + morphological cleanup |
| **Classification** | Circumference matching (hardcoded threshold=50) | Area + circularity ratios (resolution-independent) |
| **Dot positions** | First boundary point | Centroid via `cv2.moments` (more robust) |
| **Dot counting** | Python for-loops | Vectorized NumPy boolean masks |
| **Lighting** | Fails on uneven lighting (global threshold) | Handles uneven lighting (adaptive threshold) |
| **File count** | 22 files | 13 files (9 obsolete files removed) |

## How It Works

1. **Image Preprocessing** (`game_region.py`): Gaussian blur for noise reduction, adaptive Gaussian thresholding to handle uneven lighting, morphological close/open to bridge center-line gaps and remove noise.

2. **Contour Detection** (`domino_finder.py`): Uses OpenCV's `cv2.findContours` with `RETR_TREE` hierarchy to find all contours in one C-optimized call.

3. **Contour Classification** (`domino_finder.py`): Classifies contours using area and circularity (4*pi*area/perimeter^2):
   - **Dots**: Small area, high circularity (>0.45), most numerous group
   - **Center lines**: Medium area (~9x dot area), low circularity (<0.55)
   - **Noise/border**: Filtered out by minimum area and hierarchy level

4. **Dot Counting** (`domino_finder.py`): Computes centroids via `cv2.moments`, then uses vectorized NumPy masks to count dots in each domino half.

5. **Adjacency Classification** (`adj_helper.py`): Builds a relation matrix encoding spatial relationships between domino pairs using 12 relation codes.

6. **Row/Column Analysis** (`get_rows.py`, `get_cols.py`): Graph traversal to find connected rows/columns and compute dot sums.

7. **Result Annotation**: Overlays row and column sums on the original image.

## Requirements

- Python 3.8+
- NumPy
- OpenCV (opencv-python)

## Installation

```bash
cd python
pip install -r requirements.txt
```

## Usage

### Using a built-in test image (1-9)

```bash
# From the python/ directory
python -m domino_helper 4
```

The selector numbers correspond to:
| Selector | Image |
|----------|-------|
| 1 | IMG_0660.JPG |
| 2 | IMG_4421.JPG |
| 3 | IMG_4759.JPG |
| 4 | IMG_7010.JPG (default) |
| 5 | IMG_4384.JPG |
| 6 | IMG_6365.PNG |
| 7 | slantedRight.jpg |
| 8 | slantedRight.jpg |
| 9 | manyRows.jpg |

### Using a custom image

```bash
python -m domino_helper 1 /path/to/your/domino_game.jpg
```

### Tuning preprocessing parameters

```python
from domino_helper.game_region import game_region
import cv2

img = cv2.imread('path/to/image.jpg')

# Adjust for difficult lighting conditions
region = game_region(img, block_size=71, C=15, morph_kernel_size=5)
```

### As a library

```python
from domino_helper.game_region import game_region
from domino_helper.domino_finder import domino_finder
import cv2

img = cv2.imread('path/to/image.jpg')
region = game_region(img)
dominos, annotated = domino_finder(region, img)

# dominos is a numpy array of shape (N, 7):
# [top, bottom, left, right, vert(0)/hor(1), top_dots, bottom_dots]
```

## File Structure

| Python File | MATLAB Origin | Description |
|---|---|---|
| `domino_helper/main.py` | `main.m` | Entry point |
| `domino_helper/game_region.py` | `gameRegion.m` | Image preprocessing (modernized) |
| `domino_helper/domino_finder.py` | `dominoFinder.m` | Core detection pipeline (modernized) |
| `domino_helper/adj_helper.py` | `adjHelper.m` | Adjacency classification |
| `domino_helper/get_rows.py` | `getRows.m` | Row detection & sums |
| `domino_helper/get_cols.py` | `getCols.m` | Column detection & sums |
| `domino_helper/left_dom.py` | `leftDom.m` | Left neighbor lookup |
| `domino_helper/right_dom.py` | `rightDom.m` | Right neighbor lookup |
| `domino_helper/top_dom.py` | `topDom.m` | Top neighbor lookup |
| `domino_helper/bottom_dom.py` | `bottomDom.m` | Bottom neighbor lookup |
| `domino_helper/row_sum_loc.py` | `rowSumLoc.m` | Row sum text position |
| `domino_helper/col_sum_loc.py` | `colSumLoc.m` | Column sum text position |

## Notes

- Test images are in the `data/` directory at the repository root.
- The original MATLAB custom Moore tracing and experimental tracing files have been replaced by OpenCV's optimized `findContours`. The MATLAB `.m` files are still in the repo root for reference.
- Preprocessing parameters (`block_size`, `C`, `morph_kernel_size`) can be tuned per-image for difficult lighting conditions.
