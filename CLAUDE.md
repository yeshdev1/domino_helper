# Domino Helper

## Project Overview

Domino Helper is an image processing application that analyzes photos of domino games to detect dominos, count their dots, identify spatial relationships (rows and columns), compute sums, and help predict the next best move.

The project has two implementations:
- **MATLAB** (original): `.m` files in the repository root
- **Python** (port): `python/domino_helper/` package

## Architecture

### Pipeline

```
Image → Preprocessing → Boundary Tracing → Domino Detection → Adjacency Analysis → Row/Col Sums → Annotated Output
```

1. **Preprocessing** (`gameRegion.m` / `game_region.py`): 15x15 average filter → grayscale → Otsu threshold → invert
2. **Boundary Tracing** (`mooreTracing.m` / `moore_tracing.py`): Custom Moore neighborhood algorithm traces contours by scanning for white-to-black transitions
3. **Domino Detection** (`dominoFinder.m` / `domino_finder.py`): Identifies dots (most common circumference), center lines (~3x dot size), bounding boxes, orientation, and dot counts per half
4. **Adjacency** (`adjHelper.m` / `adj_helper.py`): Encodes spatial relationships between domino pairs using 12 relation codes based on orientation combinations
5. **Row/Col Analysis** (`getRows.m`, `getCols.m` / `get_rows.py`, `get_cols.py`): Graph traversal to find connected lines and compute dot sums

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
- The Moore tracing is a custom implementation (not using built-in contour detection)
- `line_length` is the estimated center line length, used as a scale factor throughout adjacency and layout calculations
- Error tolerances: `err = 0.25 * line_length` for adjacency, threshold of 50 for circumference matching, 80 for center line filtering
