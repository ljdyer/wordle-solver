import json


# ====================
def load_json(JSON_PATH):

    with open(JSON_PATH, 'r') as file:
        content = json.load(file)
    return content


# ====================
def save_json(content, JSON_PATH):

    with open(JSON_PATH, 'w') as file:
        json.dump(content, file, indent=4, sort_keys=True)
