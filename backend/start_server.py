"""
Start the FastAPI server
"""
import uvicorn
import sys
import os

# Ensure we're in the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

