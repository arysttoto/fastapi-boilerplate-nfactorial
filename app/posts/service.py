from pydantic import BaseSettings

from app.config import database

from app.auth.adapters.jwt_service import JwtService
from .repository.repository import PostRepository


class PostConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = PostConfig()


class Service:
    def __init__(
        self,
        repository: PostRepository,
        jwt_svc: JwtService,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc


def get_service():
    repository = PostRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)

    svc = Service(repository, jwt_svc)
    return svc


# from app.config import database

# from .repository.repository import TweetRepository


# class Service:
#     def __init__(
#         self,
#         repository: TweetRepository,
#     ):
#         self.repository = repository


# def get_service():
#     repository = TweetRepository(database)

#     svc = Service(repository)
#     return svc
