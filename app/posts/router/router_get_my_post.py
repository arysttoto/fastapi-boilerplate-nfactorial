from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from typing import Optional, Any

from pydantic import Field


class getPostResponse(AppModel):
    _id: Any = Field(alias="_id")
    user_id: Any = Field(alias="user_id")
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str
    location: Any
    media: Optional[list]


@router.get("/{post_id}", status_code=200, response_model=getPostResponse)
def get_post(post_id: str, svc: Service = Depends(get_service)):
    post = svc.repository.get_post_by_id(post_id)

    if not post:
        raise InvalidCredentialsException

    return post
