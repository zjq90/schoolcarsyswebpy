"""
学生路由
处理学生相关的API接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models import Student, Bus
from backend.app.schemas import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(prefix="/api/students", tags=["学生管理"])


@router.get("/", response_model=List[StudentResponse])
def get_students(
    skip: int = 0,
    limit: int = 100,
    status: Optional[bool] = None,
    bus_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取学生列表
    支持分页、状态筛选、校车筛选
    """
    query = db.query(Student).order_by(desc(Student.created_at))
    
    if status is not None:
        query = query.filter(Student.status == status)
    if bus_id:
        query = query.filter(Student.bus_id == bus_id)
    
    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    获取单个学生详情
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    return student


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    创建学生
    """
    # 检查学号是否已存在
    if student.student_number:
        existing_student = db.query(Student).filter(Student.student_number == student.student_number).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学号已存在"
            )
    
    # 检查校车是否存在
    if student.bus_id:
        existing_bus = db.query(Bus).filter(Bus.id == student.bus_id).first()
        if not existing_bus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定的校车不存在"
            )
    
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    更新学生信息
    """
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    update_data = student_update.model_dump(exclude_unset=True)
    
    # 检查学号是否已被其他学生使用
    if "student_number" in update_data and update_data["student_number"]:
        existing_student = db.query(Student).filter(
            Student.student_number == update_data["student_number"],
            Student.id != student_id
        ).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学号已被其他学生使用"
            )
    
    # 检查校车是否存在
    if "bus_id" in update_data and update_data["bus_id"]:
        existing_bus = db.query(Bus).filter(Bus.id == update_data["bus_id"]).first()
        if not existing_bus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="指定的校车不存在"
            )
    
    for key, value in update_data.items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    删除学生
    """
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    db.delete(db_student)
    db.commit()
    
    return {"message": "删除成功", "student_id": student_id}


@router.get("/stats/overview")
def get_student_stats(db: Session = Depends(get_db)):
    """
    获取学生统计
    """
    total_count = db.query(Student).count()
    active_count = db.query(Student).filter(Student.status == True).count()
    inactive_count = db.query(Student).filter(Student.status == False).count()
    
    return {
        "total": total_count,
        "active": active_count,
        "inactive": inactive_count
    }
