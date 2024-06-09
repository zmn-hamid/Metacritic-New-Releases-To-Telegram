import json
from typing import *


class CJSON:
    @staticmethod
    def _jsonize_filename(filename: str):
        return filename if filename.endswith('.json') else filename+'.json'

    @staticmethod
    def loads(filename: str):
        with open(CJSON._jsonize_filename(filename), encoding='utf-8') as f:
            foo = f.read().strip()
            return json.loads(foo if foo != '' else '{}')

    @staticmethod
    def dumps(data, filename: str) -> str:
        with open(CJSON._jsonize_filename(filename), 'w', encoding='utf-8') as f:
            f.write(CJSON.get_text(data))

    @staticmethod
    def get_text(data) -> str:
        return json.dumps(data, indent=4, ensure_ascii=False).encode('utf8').decode()

    @staticmethod
    def print(data):
        print(CJSON.get_text(data))
