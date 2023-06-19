from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from typing import Optional, Any, List

from pydantic import Field


class Post(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    location: Any


class GetPostsResponse(AppModel):
    total: int
    posts: List[Post]


@router.get("/", response_model=GetPostsResponse)
def get_posts(
    limit: int,
    offset: int,
    type: Optional[str] = None,
    rooms_count: Optional[int] = None,
    price_from: Optional[float] = None,
    price_until: Optional[float] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[float] = None,
    svc: Service = Depends(get_service),
):
    if (latitude != None or longitude != None or radius != None) and not (
        latitude != None and longitude != None and radius != None
    ):
        raise InvalidCredentialsException

    result = svc.repository.get_posts(
        limit,
        offset,
        type,
        rooms_count,
        price_from,
        price_until,
        latitude,
        longitude,
        radius,
    )
    return result
