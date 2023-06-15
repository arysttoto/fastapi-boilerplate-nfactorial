from app.config import database

from .adapters.s3_service import S3Service
from .repository.repository import PostRepository
from app.posts.adapters.here_service import HereService

import os

api_key = os.getenv("HERE_API_KEY")


class Service:
    def __init__(self):
        self.repository = PostRepository(database)
        self.s3_service = S3Service()
        self.here_service = HereService(api_key=api_key)


def get_service():
    svc = Service()
    return svc
