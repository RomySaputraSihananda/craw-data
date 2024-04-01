import uvicorn

from fastapi import FastAPI
from src.controller.lamudi import LamudiController

app: FastAPI = FastAPI(
    title='Lamudi Service', 
    version='v0.0.1', 
    description='rest api untuk mengambil data ruko dan kos dari aplikasi [lamudi.co.id](https://lamudi.co.id)',
)

app.include_router(LamudiController().router, prefix="/api/v1/lamudi", tags=["Lamudi"])

if(__name__ == "__main__"):
    uvicorn.run(app, host='0.0.0.0', port=4444)
