from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class createCommentRequest(AppModel):
    comment: str


@router.post("/{post_id}/comments", status_code=200)
def create_post_comment(
    post_id: str,
    input: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    svc.repository.create_post_comment(user_id, post_id, input)

    return 200  # success
