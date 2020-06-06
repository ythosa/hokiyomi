import json


def add_group_pic(id, bytes):
    data = _get_data()
    group = data["groups"].get(id)

    if group:
        data["groups"][id].append(bytes)
    else:
        data["groups"][id] = [bytes]

    _push_data(data)


def _push_data(data):
    with open('test_db.json', "w") as f:
        json.dump(data, f)


def _get_data():
    with open('test_db.json', "r") as f:
        data = json.load(f)
    return data
