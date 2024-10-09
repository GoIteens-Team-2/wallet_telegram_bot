import json


def write_inf(data, file_name):
    data = json.dumps(data)
    data = json.loads(str(data))

    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

data = {
    "name" : "sorrow"
}

write_inf(data, "user_info")