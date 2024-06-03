from json import loads
def start(): 
    with open('/home/romy/Desktop/dasor-皇/craw-data/src/4test/data.jsonl', 'r') as f:
        return [loads(d) for d in f.read().split('\n')]