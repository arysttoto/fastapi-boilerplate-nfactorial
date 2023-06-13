from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from app.auth.utils.security import hash_password


class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, user: dict):
        payload = {
            "type": user["type"],
            "price": user["price"],
            "address": user["address"],
            "area": user["area"],
            "rooms_count": user["rooms_count"],
            "description": user["description"],
        }
        result = self.database["posts"].insert_one(payload)
        return result.inserted_id

    # def get_user_by_id(self, user_id: str) -> dict | None:
    #     user = self.database["users"].find_one(
    #         {
    #             "_id": ObjectId(user_id),
    #         }
    #     )
    #     return user

    # def get_user_by_email(self, email: str) -> dict | None:
    #     user = self.database["users"].find_one(
    #         {
    #             "email": email,
    #         }
    #     )
    #     return user

    # def update_user(self, user_id: str, updated_data: dict):
    #     payload = {
    #         "phone": updated_data["phone"],
    #         "name": updated_data["name"],
    #         "city": updated_data["city"],
    #     }
    #     self.database["users"].update_one({"_id": ObjectId(user_id)}, {"$set": payload})
