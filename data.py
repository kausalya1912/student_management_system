import json
import os

FILE_NAME = "interns.json"

def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except:
            return []

def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)