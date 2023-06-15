from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from typing import Optional, Any

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from pydantic import Field


class Favorite(AppModel):
    _id: Any = Field(alias="_id")
    user_id: Any = Field(alias="user_id")
    post_id: Any = Field(alias="post_id")


class getFavoritesResponse(AppModel):
    favorites: list[Favorite]


@router.get("/favorites", status_code=200, response_model=getFavoritesResponse)
def get_my_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id

    favorites = svc.repository.get_favorites(user_id)

    return {"favorites": list(favorites)}
