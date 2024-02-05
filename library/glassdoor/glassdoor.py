from requests import Session, Response

class BaseGlassDoor:
    def __init__(self) -> None:
        self.__requests: Session = Session()
        self.__requests.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })

    def _get_by_detail__id(self, employer_id: int) -> None:
        ...

if(__name__ == '__main__'):
    glassdoor: BaseGlassDoor = BaseGlassDoor()
    glassdoor._get_by_employer_id(466601)
