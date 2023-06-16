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

    def create_post(self, userId, user: dict, location):
        payload = {
            "user_id": ObjectId(userId),
            "type": user["type"],
            "price": user["price"],
            "address": user["address"],
            "area": user["area"],
            "rooms_count": user["rooms_count"],
            "description": user["description"],
            "location": location,
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

    def update_post(self, postId, userId, input, location):
        post = self.database["posts"].find_one({"_id": ObjectId(postId)})

        if not post:
            raise InvalidCredentialsException
        if str(post["user_id"]) != userId:
            raise AuthorizationFailedException

        payload = {
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"],
            "location": location,
        }
        self.database["posts"].update_one({"_id": ObjectId(postId)}, {"$set": payload})

    def delete_post(self, postId, userId):
        post = self.database["posts"].find_one({"_id": ObjectId(postId)})
        if not post:
            raise InvalidCredentialsException
        if str(post["user_id"]) != userId:
            raise AuthorizationFailedException
        # delete from posts, favorites and all it's comments
        self.database["posts"].delete_one({"_id": ObjectId(postId)})
        self.database["comments"].delete_many({"post_id": ObjectId(postId)})
        self.database["favorites"].delete_many({"post_id": ObjectId(postId)})
        return

    def change_post_image(self, postId, imageLinks):
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

    def add_favorite(self, postId, userId):
        query = {"$and": [{"user_id": ObjectId(userId)}, {"post_id": ObjectId(postId)}]}
        existing = list(self.database["favorites"].find(query))
        if not existing:
            payload = {"user_id": ObjectId(userId), "post_id": ObjectId(postId)}
            self.database["favorites"].insert_one(payload)
        return

    def get_favorites(self, userId):
        favorites = self.database["favorites"].find({"user_id": ObjectId(userId)})
        return favorites

    def delete_favorite(self, postId, userId):
        query = {"$and": [{"user_id": ObjectId(userId)}, {"post_id": ObjectId(postId)}]}
        self.database["favorites"].delete_one(query)
