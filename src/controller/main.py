import uvicorn

from fastapi import FastAPI
from .test import Test

app: FastAPI = FastAPI(title='test', version='v1.0.0', description='test')

app.include_router(Test().router, prefix="/test", tags=["Google Search image"])

if(__name__ == "__main__"):
    uvicorn.run(app, port=4444)
