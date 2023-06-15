from fastapi import Depends, HTTPException, status

from app.utils import AppModel

import logging
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.delete("/{post_id}/media", status_code=200)
def delete_post_images(
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    paths = svc.repository.delete_post_images(user_id, post_id)

    if paths:
        for i in list(paths):
            svc.s3_service.delete_file(i)
    return 200
