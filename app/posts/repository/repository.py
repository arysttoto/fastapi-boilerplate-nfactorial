from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database

from fastapi.responses import JSONResponse
import logging

from app.auth.utils.security import hash_password

from ..router.errors import InvalidCredentialsException, AuthorizationFailedException


class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, userId, user: dict):
        payload = {
            "user_id": ObjectId(userId),
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

    def change_post_image(self, postId, userId, imageLinks):
        post = self.database["posts"].find_one({"_id": ObjectId(postId)})

        if not post:
            raise InvalidCredentialsException
        if post["user_id"] != userId:
            raise AuthorizationFailedException
        payload = {"media": {"$each": imageLinks}}
        self.database["posts"].update_one({"_id": ObjectId(postId)}, {"$push": payload})

    def delete_post_images(self, userId, postId):
        post = self.database["posts"].find_one({"_id": ObjectId(postId)})

        if not post:
            raise InvalidCredentialsException

        if str(post["user_id"]) != userId:
            raise AuthorizationFailedException

        media = post["media"]

        self.database["posts"].update_one(
            {"_id": ObjectId(postId)}, {"$unset": {"media": ""}}
        )

        return media

    def create_post_comment(self, userId, postId, comment):
        post = self.database["posts"].find_one({"_id": ObjectId(postId)})

        if not post:
            raise InvalidCredentialsException

        payload = {
            "content": comment,
            "created_at": datetime.utcnow(),
            "author_id": ObjectId(userId),
            "post_id": ObjectId(postId),
        }
        self.database["comments"].insert_one(payload)

    def get_post_comments(self, postId):
        comments = self.database["comments"].find({"post_id": ObjectId(postId)})
        return comments

    def change_post_comment(self, userId, postId, commentId, new_comment):
        comment = self.database["comments"].find_one({"_id": ObjectId(commentId)})

        if not comment:
            raise InvalidCredentialsException
        if str(comment["author_id"]) != userId:
            raise AuthorizationFailedException
        if str(comment["post_id"]) != postId:
            raise InvalidCredentialsException
        self.database["comments"].update_one(
            {"_id": ObjectId(commentId)}, {"$set": {"content": new_comment}}
        )

    def delete_post_comment(self, userId, postId, commentId):
        comment = self.database["comments"].find_one({"_id": ObjectId(commentId)})

        if not comment:
            raise InvalidCredentialsException
        if str(comment["author_id"]) != userId:
            raise AuthorizationFailedException
        if str(comment["post_id"]) != postId:
            raise InvalidCredentialsException
        self.database["comments"].delete_one({"_id": ObjectId(commentId)})
