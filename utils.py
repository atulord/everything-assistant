import json
import pandas as pd
import os


def load_json(file_path: str):
    with open(file_path) as file:
        loaded_dict = json.load(file)
    return loaded_dict


def load_csv(file_path: str):
    df = pd.read_csv(file_path)
    return df.to_json(orient="records")


def save_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data successfully saved to {filename}")
