from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException


class getPostResponse(AppModel):
    id_post: str
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: str


@router.get("/{item_id}", status_code=200)
def get_post(item_id: str, svc: Service = Depends(get_service)):
    post = svc.repository.get_post_by_id(item_id)
    if not post:
        raise InvalidCredentialsException
    return getPostResponse(
        id_post=str(post["_id"]),
        type=post["type"],
        price=post["price"],
        address=post["address"],
        area=post["area"],
        rooms_count=post["rooms_count"],
        description=post["description"],
        user_id=str(post["user_id"]),
    )
