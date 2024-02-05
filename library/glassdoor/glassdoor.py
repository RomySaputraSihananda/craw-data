class BaseGlassDoor:
    def __init__(self) -> None:
        ...

    def _get_by_employer_id(self, employer_id: int) -> None:
        ...

if(__name__ == '__main__'):
    glassdoor: BaseGlassDoor = BaseGlassDoor()
    glassdoor._get_by_employer_id(9079)
