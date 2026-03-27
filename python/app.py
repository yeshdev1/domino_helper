"""
FastAPI server for the Domino Helper web frontend.

Serves a mobile-friendly single-page app and provides an /api/analyze
endpoint that accepts an image upload and returns domino detection results.

Usage:
    cd python
    pip install -r requirements.txt
    uvicorn app:app --host 0.0.0.0 --port 8000
"""

import base64
from io import BytesIO

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from domino_helper.game_region import game_region
from domino_helper.domino_finder import domino_finder

app = FastAPI(title="Domino Helper")


@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    block_size: int = Query(51, description="Adaptive threshold block size (odd)"),
    c_val: int = Query(10, description="Adaptive threshold constant"),
    morph_size: int = Query(3, description="Morphological kernel size"),
):
    """Analyze a domino game image and return detection results."""
    # Read and decode image from upload (no temp files)
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=422, detail="Could not decode image. Please upload a valid JPEG or PNG.")

    # Run the detection pipeline
    try:
        region = game_region(img, block_size=block_size, C=c_val, morph_kernel_size=morph_size)
        dominos, annotated, rows, row_sums, cols, col_sums = domino_finder(region, img)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Analysis failed: {str(e)}")

    # Encode annotated image as JPEG base64
    _, buf = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])
    img_b64 = base64.b64encode(buf.tobytes()).decode('utf-8')

    # Build structured domino data
    num_dominos = dominos.shape[0]
    domino_list = []
    for i in range(num_dominos):
        d = dominos[i]
        domino_list.append({
            "index": i,
            "orientation": "horizontal" if d[4] == 1 else "vertical",
            "top_left_dots": int(d[5]),
            "bottom_right_dots": int(d[6]),
            "total": int(d[5] + d[6]),
        })

    row_list = []
    for i in range(len(row_sums)):
        row_list.append({
            "index": i,
            "sum": int(row_sums[i]),
            "num_dominos": rows[i].shape[1] if i < len(rows) else 0,
        })

    col_list = []
    for i in range(len(col_sums)):
        col_list.append({
            "index": i,
            "sum": int(col_sums[i]),
            "num_dominos": cols[i].shape[1] if i < len(cols) else 0,
        })

    return {
        "num_dominos": num_dominos,
        "dominos": domino_list,
        "rows": row_list,
        "cols": col_list,
        "annotated_image": f"data:image/jpeg;base64,{img_b64}",
    }


# Serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return FileResponse("static/index.html")
