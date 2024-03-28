from http import HTTPStatus

class BodyResponse:
    def __init__(self, status_code: HTTPStatus, data: list, **kwagrs) -> None:
        self.status: str = status_code.phrase
        self.code: int = status_code.value
        self.message: str = kwagrs.get('message', status_code.description)
        self.data: list = data
        
        if(data): self.data_length: int = len(data) if data else None
        if(kwagrs):
            for keyword in kwagrs:
                self.__dict__[keyword] = kwagrs.get(keyword)
