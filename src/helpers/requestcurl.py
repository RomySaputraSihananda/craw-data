from urllib.parse import urlencode
from subprocess import run, CompletedProcess

class RequestsCurl:
    def __init__(self, url, method='GET', params=None, headers=None, data=None) -> CompletedProcess:
        self.url = url
        self.method = method.upper()
        self.params = params
        self.headers = headers
        self.data = data
        header, text = self.build()
        self.text = text
        self.headers = {}
        for header in header.split('\r\n')[1:]:
            key, value = header.split(': ', 1)
            self.headers[key] = value

    def build(self):
        command = ["curl", "-i"]

        command.append("-X")
        command.append(self.method)

        if self.headers:
            for key, value in self.headers.items():
                command.append("-H")
                command.append(f"{key}: {value}")

        if self.params:
            params_str = urlencode(self.params)
            self.url += f"?{params_str}"

        command.append(self.url)

        if self.data:
            command.append("--data-raw")
            command.append(f'{urlencode(self.data)}')
        
        completed_process = run(command, capture_output=True)
        print(completed_process)
        return completed_process.stdout.decode().strip().split('\r\n\r\n', 1)

class requests:
    @staticmethod
    def get(url, params=None, headers=None, data=None) -> CompletedProcess:
        return RequestsCurl(url, 'GET', params, headers, data)
    
    @staticmethod
    def post(url, params=None, headers=None, data=None) -> CompletedProcess:
        return RequestsCurl(url, 'POST', params, headers, data)
        