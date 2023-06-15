from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

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
def create_post(
    input: createPostRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    coordinates = svc.here_service.get_coordinates(address=input.address)
    if not coordinates:
        coordinates = "Unknown"

    id_post = svc.repository.create_post(user_id, input.dict(), coordinates)

    return createPostResponse(new_post_id=str(id_post))
