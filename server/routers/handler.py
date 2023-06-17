from fastapi import APIRouter, Request, Depends, Header
from sqlmodel import Session
from utils.db import get_session
from models import Callback, CallbackHistory
import datetime
import json
from utils.mqtt import publish_message
import os

TESTING = os.getenv("TESTING", 0)


router = APIRouter(
    prefix="/handle",
    tags=["Hanlder"],
)

def format_header(header: Header):
    """Format header from request"""
    return json.dumps(dict(header))

async def _handle(request: Request, path: str, session: Session ):
    """Handle this method for handle all request
    flow -> user access /handle/{path} with method get, post, put
    get callback by path
    check callback is exist or not
    if callback is exist
    send request (body, header) to path mqtt
    """
    callback = session.query(Callback).filter(Callback.path == path).first()
    request_body = (await request.body()).decode("utf-8")
    request_header = format_header(request.headers)
    if callback is None:
        return {
            "body": request_body,
            "header": request_header,
            "message": "Callback not found",
            "method": request.method,
        }
    
    callback_history = CallbackHistory(
        callback_id=callback.id,
        body=request_body,
        headers=request_header,
        method=request.method,
        timestamp=datetime.datetime.now()
    )

    message = {
        "body": request_body,
        "header": request_header,
        "method": request.method,
    }
    if not TESTING:
        publish_message(callback.path, json.dumps(message))

    session.add(callback_history)
    session.commit()

    return "OK"

@router.get("/{path}")
async def handle(request: Request, path: str, session: Session = Depends(get_session)):
    return await _handle(request, path, session)

@router.post("/{path}")
async def handle(request: Request, path: str, session: Session = Depends(get_session)):
    return await _handle(request, path, session)

@router.put("/{path}")
async def handle(request: Request, path: str, session: Session = Depends(get_session)):
    return await _handle(request, path, session)

