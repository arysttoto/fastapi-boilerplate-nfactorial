from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from app.auth.utils.security import hash_password

from ..router.errors import InvalidCredentialsException, AuthorizationFailedException


class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, userId: str, user: dict):
        payload = {
            "user_id": userId,
            "type": user["type"],
            "price": user["price"],
            "address": user["address"],
            "area": user["area"],
            "rooms_count": user["rooms_count"],
            "description": user["description"],
        }
        result = self.database["posts"].insert_one(payload)
        return result.inserted_id

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_post_by_id(self, post_id: str):
        post = self.database["posts"].find_one({"_id": ObjectId(post_id)})
        return post

    def update_post(self, postId, userId, input):
        post = self.database["posts"].find_one({"_id": ObjectId(postId)})

        if not post:
            raise InvalidCredentialsException
        if post["user_id"] != userId:
            raise AuthorizationFailedException

        payload = {
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"],
        }
        self.database["posts"].update_one({"_id": ObjectId(postId)}, {"$set": payload})

    def delete_post(self, postId, userId):
        post = self.database["posts"].find_one({"_id": ObjectId(postId)})
        if not post:
            raise InvalidCredentialsException
        if post["user_id"] != userId:
            raise AuthorizationFailedException
        self.database["posts"].delete_one({"_id": ObjectId(postId)})
