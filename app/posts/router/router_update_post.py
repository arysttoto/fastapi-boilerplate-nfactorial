from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
from .errors import InvalidCredentialsException


class updatePostRequest(AppModel):
    type: str
    price: float
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{post_id}", status_code=200)
def update_post(
    post_id: str,
    input: updatePostRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id

    coordinates = svc.here_service.get_coordinates(address=input.address)
    if not coordinates:
        coordinates = "Unknown"

    svc.repository.update_post(post_id, user_id, input.dict(), coordinates)

    return 200
