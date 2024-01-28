import os
from json import dumps
class Iostream:
    def write_json(file_path: str, data: dict) -> None:
        directory: str = os.path.dirname(file_path)

        if not os.path.isdir(directory) and bool(directory):
            os.makedirs(directory)

        with open(file_path, 'w') as file:
            file.write(dumps(data, indent=4, ensure_ascii=False))
        
        print(file_path)
    

# testing
if(__name__ == '__main__'):
    Iostream.write_file('o.json', {"memek":"dshfh"})