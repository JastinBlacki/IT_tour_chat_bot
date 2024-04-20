import json
from config import DATA_PATH


def read_inf(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)


def get_message(id):
    mes_file = read_inf(DATA_PATH)
    start_mes = mes_file[id].get('text')
    return start_mes
