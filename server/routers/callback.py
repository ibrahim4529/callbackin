from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from utils.db import get_session
from utils.jwt import get_current_user
from models import User, Callback
from schemas.callback import CallbackCreate, CallbackRead


router = APIRouter(
    prefix="/callbacks",
    tags=["callbacks"],
)


@router.post("/", response_model=CallbackRead)
async def create_callback(request: CallbackCreate,
                          session: Session = Depends(get_session),
                          user: User = Depends(get_current_user)):
    """Create Callback this method for create callback
    flow -> user access /callbacks with method post and send data
    and this endpoint will be create callback on database
    and return callback data
    """
    callback = Callback(**request.dict(), user_id=user.id)
    session.add(callback)
    session.commit()
    session.refresh(callback)
    return callback


@router.get("/", response_model=list[CallbackRead])
async def get_callbacks(session: Session = Depends(get_session),
                        user: User = Depends(get_current_user)):
    """Get Callbacks this method for get all callbacks
    flow -> user access /callbacks with method get
    and this endpoint will be get all callbacks on database from user
    and return all callbacks data
    """
    callbacks = session.query(Callback).filter(
        Callback.user_id == user.id).all()
    return callbacks


@router.get("/{callback_id}", response_model=CallbackRead)
async def get_callback(callback_id: int,
                       user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """Get Callback this method for get callback by id
    flow -> user access /callbacks/{callback_id} with method get
    check callback id is exist or not
    check callback id is belong to user or not
    and return callback data
    """
    callback = session.query(Callback).filter(
        Callback.id == callback_id, Callback.user_id == user.id).first()
    if callback is None:
        raise HTTPException(status_code=404, detail="Callback not found")
    return callback