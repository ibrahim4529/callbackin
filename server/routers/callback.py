from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from utils.db import get_session
from utils.jwt import get_current_user
from models import User, Callback
from schemas.callback import CallbackCreate, CallbackRead, CallbackUpdate


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


@router.put("/{callback_id}", response_model=CallbackRead)
async def update_callback(callback_id: int,
                          request: CallbackUpdate,
                          session: Session = Depends(get_session),
                          user: User = Depends(get_current_user)):
    """Update Callback this method for update callback by id
    flow -> user access /callbacks/{callback_id} with method put
    check callback id is exist or not
    check callback id is belong to user or not
    and update callback data
    """
    callback: Callback | None = session.query(Callback).filter(
        Callback.id == callback_id, Callback.user_id == user.id).first()
    if callback is None:
        raise HTTPException(status_code=404, detail="Callback not found")
    callback.name = request.name if request.name else callback.name
    callback.description = request.description if request.description else callback.description
    callback.local_endpoint = request.local_endpoint if request.local_endpoint else callback.local_endpoint
    session.add(callback)
    session.commit()
    session.refresh(callback)
    return callback


@router.delete("/{callback_id}", status_code=204)
async def delete_callback(callback_id: int,
                          user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    """Delete Callback this method for delete callback by id
    flow -> user access /callbacks/{callback_id} with method delete
    check callback id is exist or not
    check callback id is belong to user or not
    and delete callback data
    """
    callback = session.query(Callback).filter(
        Callback.id == callback_id, Callback.user_id == user.id).first()
    if callback is None:
        raise HTTPException(status_code=404, detail="Callback not found")
    session.delete(callback)
    session.commit()
    return None


@router.get("/{callback_id}/run", response_model=CallbackRead)
async def run_callback(callback_id: int,
                       user: User = Depends(get_current_user),
                       session: Session = Depends(get_session)):
    """Run Callback this method for run callback by id
    flow -> user access /callbacks/{callback_id}/run with method post
    check callback id is exist or not
    check callback id is belong to user or not
    subscribe topic based on callback path
    change callback is_running to True
    and return callback data
    """
    callback = session.query(Callback).filter(
        Callback.id == callback_id, Callback.user_id == user.id).first()
    if callback is None:
        raise HTTPException(status_code=404, detail="Callback not found")
    callback.is_running = True
    session.add(callback)
    session.commit()
    session.refresh(callback)
    return callback


@router.get("/{callback_id}/stop", response_model=CallbackRead)
async def stop_callback(callback_id: int,
                        user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    """Stop Callback this method for stop callback by id
    flow -> user access /callbacks/{callback_id}/stop with method post
    check callback id is exist or not
    check callback id is belong to user or not
    unsubscribe topic based on callback path
    change callback is_running to False
    and return callback data
    """
    callback = session.query(Callback).filter(
        Callback.id == callback_id, Callback.user_id == user.id).first()
    if callback is None:
        raise HTTPException(status_code=404, detail="Callback not found")
    callback.is_running = False
    session.add(callback)
    session.commit()
    session.refresh(callback)
    return callback
    
