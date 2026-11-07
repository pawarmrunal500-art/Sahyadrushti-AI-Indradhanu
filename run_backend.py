"""
Run script for SAHYADRUSHTI AI FastAPI Backend Server
"""
import sys
import os
import uvicorn

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    print("Starting SAHYADRUSHTI AI Backend on http://127.0.0.1:8000 ...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
