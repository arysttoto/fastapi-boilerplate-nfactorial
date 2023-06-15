from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router

from .errors import InvalidCredentialsException

from typing import Optional, Any

from pydantic import Field

import json
from fastapi.responses import JSONResponse


class Comment(AppModel):
    id_comment: Optional[Any] = Field(alias="_id")
    content: Optional[str]
    created_at: Optional[Any]
    author_id: Optional[Any] = Field(alias="author_id")
    post_id: Optional[Any] = Field(alias="post_id")


class getCommentResponse(AppModel):
    comments: list[Comment]


@router.get("/{post_id}/comments", status_code=200, response_model=getCommentResponse)
def get_post_comments(post_id: str, svc: Service = Depends(get_service)):
    post = svc.repository.get_post_by_id(post_id)

    if not post:
        raise InvalidCredentialsException

    comments = svc.repository.get_post_comments(post_id)

    return {"comments": list(comments)}
