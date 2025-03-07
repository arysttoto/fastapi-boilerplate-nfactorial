from typing import Any, Optional

import logging

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from .errors import InvalidCredentialsException


class GetMyAccountResponse(AppModel):
    id: Any = Field(alias="_id")
    email: str
    city: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    avatar_url: Optional[str]


@router.get("/users/me", response_model=GetMyAccountResponse)
def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user = svc.repository.get_user_by_id(jwt_data.user_id)
    # logging.info(user)
    if not user:
        raise InvalidCredentialsException

    return user
