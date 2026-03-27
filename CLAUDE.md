# Domino Helper

## Project Overview

Domino Helper is an image processing application that analyzes photos of domino games to detect dominos, count their dots, identify spatial relationships (rows and columns), compute sums, and help predict the next best move.

The project has two implementations:
- **MATLAB** (original): `.m` files in the repository root — uses custom Moore tracing, circumference-based classification
- **Python** (modernized): `python/domino_helper/` package — uses OpenCV-optimized contour detection, area+circularity classification

## Architecture

### Pipeline

```
Image → Preprocessing → Contour Detection → Domino Detection → Adjacency Analysis → Row/Col Sums → Annotated Output
```

### MATLAB (original)

1. **Preprocessing** (`gameRegion.m`): 15x15 average filter → grayscale → Otsu threshold → invert
2. **Boundary Tracing** (`mooreTracing.m`): Custom Moore neighborhood algorithm (pixel-by-pixel in MATLAB)
3. **Classification**: Circumference matching (threshold of 50) to find dots, center lines at ~3x dot circumference
4. **Dot Counting**: First boundary point used as dot position

### Python (modernized)

1. **Preprocessing** (`game_region.py`): Gaussian blur → adaptive Gaussian threshold → morphological close/open cleanup
   - Adaptive threshold handles uneven lighting (global Otsu cannot)
   - Morphological ops bridge center-line gaps and remove noise
   - Tunable: `block_size`, `C`, `morph_kernel_size` parameters
2. **Contour Detection** (`domino_finder.py`): `cv2.findContours` with `RETR_TREE` hierarchy
   - C-optimized, orders of magnitude faster than pure-Python Moore tracing
   - Hierarchy gives parent-child relationships (dots inside dominos)
3. **Classification**: Area + circularity (4*pi*area/perimeter^2)
   - Dots: small area, high circularity (>0.45) — resolution-independent via ratios
   - Center lines: medium area (~9x dot area), low circularity (<0.55)
   - Noise/border: filtered by minimum area and hierarchy level
4. **Dot Counting**: Centroid via `cv2.moments` (more robust than first boundary point)
   - Vectorized NumPy mask operations for half-assignment
5. **Adjacency** (`adj_helper.py`): Unchanged — encodes spatial relationships using 12 relation codes
6. **Row/Col Analysis** (`get_rows.py`, `get_cols.py`): Unchanged — graph traversal for connected lines

### Key Data Structure

Each domino is a 7-element vector: `[top, bottom, left, right, vert(0)/hor(1), top_left_dots, bottom_right_dots]`

### Adjacency Relation Codes

- **Two Verticals**: 1=SameColTop, 2=SameColBottom, 3=SameRowTopRight, 4=SameRowTopLeft, 5=SameRowBottomRight, 6=SameRowBottomLeft
- **Two Horizontals**: 1=SameRowRight, 2=SameRowLeft, 3=SameColTopRight, 4=SameColTopLeft, 5=SameColBottomRight, 6=SameColBottomLeft
- **Vert & Hor**: 1-6 (row relations), 7-12 (column relations)

### Row/Col Orientation Codes

- Rows: 1=horizontal, 2=TopVertical, 3=BottomVertical, 4=MiddleVertical
- Cols: 1=vertical, 2=TopHorizontal, 3=BottomHorizontal, 4=MiddleHorizontal

## Running

### MATLAB
Open `main.m` in MATLAB, set the `selector` variable (1-9), and run.

### Python
```bash
cd python
pip install -r requirements.txt
python -m domino_helper [selector] [optional_image_path]
```

## Test Images

Located in `data/` directory. Use selector 1-9 in `main.m` or `python -m domino_helper <n>`.

## Key Conventions

- MATLAB uses 1-based indexing; Python port uses 0-based indexing
- MATLAB returns 0 for "not found"; Python returns -1 for "not found" in neighbor lookups
- Python uses `cv2.findContours` (C-optimized); MATLAB uses custom Moore tracing
- Python classifies by area+circularity ratios; MATLAB uses absolute circumference thresholds
- `line_length` is the median center line length, used as a scale factor throughout adjacency and layout calculations
- Error tolerances: `err = 0.25 * line_length` for adjacency matching
- Binary image: Python uses 0/255 (OpenCV convention); MATLAB uses 0/1
