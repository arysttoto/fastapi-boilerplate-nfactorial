from fastapi import Depends, HTTPException, status

from app.utils import AppModel


from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


class createCommentRequest(AppModel):
    comment: str


@router.delete("/{post_id}/comments/{comment_id}", status_code=200)
def delete_post_comment(
    post_id: str,
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    svc.repository.delete_post_comment(user_id, post_id, comment_id)

    return 200  # success
