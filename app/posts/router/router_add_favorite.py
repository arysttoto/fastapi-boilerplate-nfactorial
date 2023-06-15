from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from typing import Optional, Any

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


@router.get("/{post_id}/favorites", status_code=200)
def add_post_to_favorites(
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    post = svc.repository.get_post_by_id(post_id)
    if not post:
        return InvalidCredentialsException

    svc.repository.add_favorite(post_id, user_id)

    return 200
