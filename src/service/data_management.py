import json

class DataManager:
    def __init__(self) -> None:
        self.user_data = {}

    def load_user_data(self, user_id):
        file_name = f"data/user_{user_id}_data.json"
        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                self.user_data[user_id] = json.load(file)
        except FileNotFoundError:
            self.user_data[user_id] = {"balance": 0, "transactions": []}

    def save_user_data(self, user_id):
        file_name = f"data/user_{user_id}_data.json"
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(self.user_data[user_id], file, indent=4)


data_manager = DataManager()