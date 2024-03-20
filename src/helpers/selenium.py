from seleniumwire.utils import decode

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire.webdriver import Chrome as _Chrome
from seleniumwire.webdriver import Firefox as _Firefox

class Chrome(_Chrome):
    def __init__(self, *args, seleniumwire_options=None, **kwargs):
        super().__init__(*args, seleniumwire_options=seleniumwire_options, **kwargs)
    
    def find_element(self, by=By.ID, value: str | None = None, timeout: int = 10) -> WebElement:
        return WebDriverWait(super(), timeout).until(EC.presence_of_element_located((by, value)))
    
    def find_elements(self, by=By.ID, value: str | None = None, timeout: int = 10) -> EC.List[WebElement]:
        return WebDriverWait(super(), timeout).until(EC.presence_of_all_elements_located((by, value)))

    def add_cookie(self, cookie: dict) -> None:
        return super().add_cookie(cookie)
        
    def add_cookies(self, cookies: list) -> None:
        for cookie in cookies: super().add_cookie(cookie)

class Firefox(_Firefox):
    def __init__(self, *args, seleniumwire_options=None, **kwargs):
        super().__init__(*args, seleniumwire_options=seleniumwire_options, **kwargs)
    
    def find_element(self, by=By.ID, value: str | None = None, timeout: int = 10) -> WebElement:
        return WebDriverWait(super(), timeout).until(EC.presence_of_element_located((by, value)))
    
    def find_elements(self, by=By.ID, value: str | None = None, timeout: int = 10) -> EC.List[WebElement]:
        return WebDriverWait(super(), timeout).until(EC.presence_of_all_elements_located((by, value)))

    def add_cookie(self, cookie: dict) -> None:
        return super().add_cookie(cookie)
        
    def add_cookies(self, cookies: list) -> None:
        for cookie in cookies: super().add_cookie(cookie)

if(__name__ == '__main__'):
    baseSelenium: Chrome = Chrome()
    baseSelenium.get('https://google.com')

    search = baseSelenium.find_element(By.NAME, 'q')
    search.send_keys("google search through python")
    search.send_keys(Keys.RETURN)
    baseSelenium.quit()

