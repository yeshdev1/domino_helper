# Domino Helper - Python

A Python port of the MATLAB Domino Helper project. Takes a picture of an ongoing dominos game and analyzes the board to detect dominos, count dots, identify rows and columns, and compute sums to help predict the next best move.

## How It Works

1. **Image Preprocessing** (`game_region.py`): Applies a 15x15 averaging filter, converts to grayscale, applies Otsu's thresholding, and inverts the binary image to isolate domino features.

2. **Boundary Tracing** (`moore_tracing.py`, `get_neighbourhood.py`): Custom Moore neighborhood boundary tracing scans the binary image for white-to-black transitions and traces each contour. This replaces MATLAB's `bwboundaries`.

3. **Domino Detection** (`domino_finder.py`): Identifies circles (dots) by finding the most common boundary circumference. Center lines are detected as boundaries ~3x the circle size. Each domino's bounding box, orientation (vertical/horizontal), and dot counts per half are extracted.

4. **Adjacency Classification** (`adj_helper.py`): Builds a relation matrix encoding how each pair of dominos is spatially positioned (same row, same column, relative positions).

5. **Row/Column Analysis** (`get_rows.py`, `get_cols.py`): Traverses the adjacency graph to find connected rows and columns, computing the sum of dots along each line.

6. **Result Annotation**: Overlays row and column sums on the original image.

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

## File Mapping (MATLAB to Python)

| MATLAB File | Python File | Description |
|---|---|---|
| `main.m` | `domino_helper/main.py` | Entry point |
| `gameRegion.m` | `domino_helper/game_region.py` | Image preprocessing |
| `dominoFinder.m` | `domino_helper/domino_finder.py` | Core domino detection |
| `mooreTracing.m` | `domino_helper/moore_tracing.py` | Boundary tracing |
| `getNeighbourhood.m` | `domino_helper/get_neighbourhood.py` | Moore neighborhood lookup |
| `adjHelper.m` | `domino_helper/adj_helper.py` | Adjacency classification |
| `getRows.m` | `domino_helper/get_rows.py` | Row detection & sums |
| `getCols.m` | `domino_helper/get_cols.py` | Column detection & sums |
| `leftDom.m` | `domino_helper/left_dom.py` | Left neighbor lookup |
| `rightDom.m` | `domino_helper/right_dom.py` | Right neighbor lookup |
| `topDom.m` | `domino_helper/top_dom.py` | Top neighbor lookup |
| `bottomDom.m` | `domino_helper/bottom_dom.py` | Bottom neighbor lookup |
| `rowSumLoc.m` | `domino_helper/row_sum_loc.py` | Row sum text position |
| `colSumLoc.m` | `domino_helper/col_sum_loc.py` | Column sum text position |
| `cornerDetector.m` | `domino_helper/corner_detector.py` | Alt detection (contour-based) |
| `theoTracing.m` | `domino_helper/theo_tracing.py` | Alt tracing (experimental) |
| `getTheoNeighbourhood.m` | `domino_helper/get_theo_neighbourhood.py` | Alt neighborhood lookup |
| `leftlookup.m` | `domino_helper/left_lookup.py` | Left pixel lookup |
| `rightLook.m` | `domino_helper/right_look.py` | Right pixel lookup |
| `upLook.m` | `domino_helper/up_look.py` | Up pixel lookup |
| `downLook.m` | `domino_helper/down_look.py` | Down pixel lookup |

## Notes

- The test images are in the `data/` directory at the repository root.
- The Moore tracing algorithm is a faithful port of the custom MATLAB implementation (not using OpenCV's `findContours`).
- The `corner_detector.py` and `theo_tracing.py` files are alternative/experimental implementations included for completeness.
