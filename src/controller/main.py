import uvicorn

from fastapi import FastAPI
from src.controller.lamudi import LamudiController

class Controllers:
    def __init__(self, **kwargs) -> None:
        self.__app: FastAPI = FastAPI(
            title=kwargs.get('title'), 
            version=kwargs.get('version'),
            description=kwargs.get('description')
        )
    
    def lamudi(self, **kwargs) -> FastAPI:
        self.__app.include_router(LamudiController().router, prefix="/api/v1/lamudi", tags=["Lamudi"])
        uvicorn.run(self.__app, host='0.0.0.0', port=kwargs.get('port', 4444))
        

# app.include_router(LamudiController().router, prefix="/api/v1/lamudi", tags=["Lamudi"])

if(__name__ == "__main__"):
    Controllers(
        title='Lamudi Service', 
        version='v0.0.1',
        description='rest api untuk mengambil data ruko dan kos dari aplikasi [lamudi.co.id](https://lamudi.co.id)',
    ).lamudi()