import uvicorn

from fastapi import FastAPI
from src.controller.lamudi import LamudiController
from src.controller.dephubgoid import DephubgoidController

class Controllers:
    def __init__(self, **kwargs) -> None:
        match(kwargs.get('web_app')):
            case 'lamudi':
                self.__set_app(
                    title='Lamudi Service', 
                    version='v0.0.1',
                    description='rest api untuk mengambil data ruko dan kos dari aplikasi [lamudi.co.id](https://lamudi.co.id)'
                )
                self.lamudi(**kwargs)
            case 'dephubgoid':
                self.__set_app(
                    title='Dephubgoid Kapal Service', 
                    version='v0.0.1',
                    description='rest api untuk mengambil data kapal dari [dephub.go.id](https://kapal.dephub.go.id)'
                )
                self.dephubgoid(**kwargs)
    
    def __set_app(self, **kwargs) -> None:
        self.__app: FastAPI = FastAPI(
            title=kwargs.get('title'), 
            version=kwargs.get('version'),
            description=kwargs.get('description')
        )

    def lamudi(self, **kwargs) -> None:
        self.__app.include_router(LamudiController().router, prefix="/api/v1/lamudi", tags=["Lamudi"])
        uvicorn.run(self.__app, host='0.0.0.0' if(kwargs.get('local')) else 'localhost', port=kwargs.get('port', 4444))
    
    def dephubgoid(self, **kwargs) -> None:
        self.__app.include_router(DephubgoidController().router, prefix="/api/v1/dephubgoid", tags=["dephubgoid"])
        uvicorn.run(self.__app, host='0.0.0.0' if(kwargs.get('local')) else 'localhost', port=kwargs.get('port', 4444))

if(__name__ == "__main__"):
    Controllers(
        title='Lamudi Service', 
        version='v0.0.1',
        description='rest api untuk mengambil data ruko dan kos dari aplikasi [lamudi.co.id](https://lamudi.co.id)',
    ).lamudi()