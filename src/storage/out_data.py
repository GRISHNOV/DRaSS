import time

from storage.user_data import get_user_data


def output_data(MK, storage_name):
    data = get_user_data(MK, storage_name)
    for element in data:
        result = ""
        chunks, chunk_size = len(element), 4
        for symbols in [element[i:i+chunk_size] for i in range(0, chunks, chunk_size)]:
            result += f"{chr(int(symbols))}"
        data_clear = dict()
        for item in result.split(";;"):
            elem = item.split("::")
            if elem[0] == "":
                continue
            if len(elem) == 2:
                data_clear[elem[0]] = elem[1]
            else:
                data_clear[elem[0]] = ""
        print(data_clear)
    input()
