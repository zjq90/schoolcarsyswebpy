from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Capture, CaptureType, User
from schemas import CaptureCreate, CaptureUpdate, CaptureResponse
from routers.auth import get_current_active_user

router = APIRouter(prefix="/api/captures", tags=["异常抓拍"])


@router.get("/", response_model=List[CaptureResponse])
async def get_captures(
    skip: int = 0,
    limit: int = 100,
    capture_type: str = None,
    is_uploaded: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Capture)
    if capture_type:
        query = query.filter(Capture.capture_type == capture_type)
    if is_uploaded is not None:
        query = query.filter(Capture.is_uploaded == is_uploaded)
    captures = query.order_by(Capture.created_at.desc()).offset(skip).limit(limit).all()
    return captures


@router.get("/{capture_id}", response_model=CaptureResponse)
async def get_capture(
    capture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    capture = db.query(Capture).filter(Capture.id == capture_id).first()
    if capture is None:
        raise HTTPException(status_code=404, detail="抓拍记录不存在")
    return capture


@router.post("/", response_model=CaptureResponse, status_code=status.HTTP_201_CREATED)
async def create_capture(
    capture_data: CaptureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    new_capture = Capture(**capture_data.model_dump())
    db.add(new_capture)
    db.commit()
    db.refresh(new_capture)
    return new_capture


@router.put("/{capture_id}", response_model=CaptureResponse)
async def update_capture(
    capture_id: int,
    capture_data: CaptureUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    capture = db.query(Capture).filter(Capture.id == capture_id).first()
    if capture is None:
        raise HTTPException(status_code=404, detail="抓拍记录不存在")
    update_data = capture_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(capture, key, value)
    if capture_data.is_uploaded:
        capture.uploaded_at = datetime.utcnow()
    db.commit()
    db.refresh(capture)
    return capture


@router.delete("/{capture_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_capture(
    capture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    capture = db.query(Capture).filter(Capture.id == capture_id).first()
    if capture is None:
        raise HTTPException(status_code=404, detail="抓拍记录不存在")
    db.delete(capture)
    db.commit()


@router.post("/{capture_id}/upload", response_model=CaptureResponse)
async def upload_capture(
    capture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    capture = db.query(Capture).filter(Capture.id == capture_id).first()
    if capture is None:
        raise HTTPException(status_code=404, detail="抓拍记录不存在")
    capture.is_uploaded = 1
    capture.uploaded_at = datetime.utcnow()
    db.commit()
    db.refresh(capture)
    return capture


@router.get("/statistics/overview")
async def get_capture_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    total = db.query(Capture).count()
    uploaded = db.query(Capture).filter(Capture.is_uploaded == 1).count()
    by_type = {}
    for capture_type in CaptureType:
        count = db.query(Capture).filter(Capture.capture_type == capture_type).count()
        by_type[capture_type.value] = count
    return {
        "total": total,
        "uploaded": uploaded,
        "not_uploaded": total - uploaded,
        "by_type": by_type
    }
