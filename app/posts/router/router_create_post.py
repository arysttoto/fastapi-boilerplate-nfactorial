from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class createPostRequest(AppModel):
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str


class createPostResponse(AppModel):
    new_post_id: str


@router.post("/", status_code=200)
def create_post(input: createPostRequest, svc: Service = Depends(get_service)):
    id_post = svc.repository.create_post(input.dict())

    return createPostResponse(new_post_id=str(id_post))
