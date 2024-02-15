from library import BaseTaptap, AbstractTaptap

class Taptap(BaseTaptap, AbstractTaptap):
    def __init__(self) -> None:
        super().__init__()
    
    def get_all_platform(self, *args, **kwargs) -> None:
        ...
    
    def get_by_platform(self, *args, **kwargs) -> None:
        ...
    
    def get_by_app_id(self, *args, **kwargs) -> None:
        ...