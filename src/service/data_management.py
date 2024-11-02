import json
import os

class DataManager:
    def __init__(self) -> None:
        self.user_data = {}
        if not os.path.exists("users_transactions"):
            os.makedirs("users_transactions")

    def load_user_data(self, user_id):
        file_name = f"users_transactions/user_{user_id}_data.json"
        try:
            with open(file_name, 'r', encoding="utf-8") as file:
                self.user_data[user_id] = json.load(file)
        except FileNotFoundError:
            self.user_data[user_id] = {"balance": 0, "transactions": []}

    def load_user_data(self, user_id):
        file_name = f"users_transactions/user_{user_id}_data.json"
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(self.user_data[user_id], file, indent=4)


data_manager = DataManager()
