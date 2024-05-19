import json

def load_data(path):
    with open(path) as file:
        data = json.load(file)
    return data

def save_data(path, data):
    with open(path, "w") as file:
        json.dump(data, file)
