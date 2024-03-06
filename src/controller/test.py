from fastapi import APIRouter

class Test:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.get('/search')(self.__search_image_by_url)
    
    def __search_image_by_url(self, url_image: str = None) -> str:
        return url_image
