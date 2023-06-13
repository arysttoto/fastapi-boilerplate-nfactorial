from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.delete("/{post_id}", status_code=200)
def delete_post(
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = svc.repository.get_user_by_id(jwt_data.user_id)["_id"]
    svc.repository.delete_post(post_id, user_id)

    return 200
