import uvicorn

from fastapi import FastAPI
from .test import Test
from src.controller.lamudi import LamudiController

app: FastAPI = FastAPI(title='Service', version='v1.0.0', description='Bukan service BE')

# app.include_router(Test().router, prefix="/api/v1/test", tags=["Google Search image"])
app.include_router(LamudiController().router, prefix="/api/v1/lamudi", tags=["Lamudi"])

if(__name__ == "__main__"):
    uvicorn.run(app, host='0.0.0.0', port=4444)
