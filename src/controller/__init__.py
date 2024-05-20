import uvicorn

from fastapi import FastAPI

from .lamudi import LamudiController
from .dephubgoid import DephubgoidController 
from .jiexpocomevent import JiexpocomEventController

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
            case 'jiexpocomevent': 
                self.__set_app(
                    title='Jiexpocom Event Service', 
                    version='v0.0.1',
                    description='rest api untuk mengambil data event dari [exhibition.jiexpo.com](https://exhibition.jiexpo.com/event-directory/)'
                )
                self.jiexpocomevent(**kwargs)
    
    def __set_app(self, **kwargs) -> None:
        self.__app: FastAPI = FastAPI(
            title=kwargs.get('title'), 
            version=kwargs.get('version'),
            description=kwargs.get('description')
        )
    
    def jiexpocomevent(self, **kwargs) -> None:
        self.__app.include_router(JiexpocomEventController().router, prefix="/api/v1/jiexpocomevent", tags=["jiexpocom"])
        uvicorn.run(self.__app, host='0.0.0.0' if(kwargs.get('local')) else 'localhost', port=kwargs.get('port', 4444))

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