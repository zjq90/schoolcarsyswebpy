"""
学生管理路由模块
处理学生的增删改查功能
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.routers.auth import get_current_user
from app.config import ROLES

router = APIRouter(prefix="/api/students", tags=["学生管理"])


@router.get("/", response_model=List[StudentResponse])
def get_students(
    skip: int = 0,
    limit: int = 100,
    school_id: Optional[int] = None,
    grade: Optional[str] = None,
    class_name: Optional[str] = None,
    route_id: Optional[int] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取学生列表
    教育局管理员可以查看所有学生，学校管理员只能查看本校学生
    """
    query = db.query(Student)
    
    # 权限控制：学校管理员只能看本校学生
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Student.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Student.school_id == school_id)
    
    # 年级过滤
    if grade:
        query = query.filter(Student.grade == grade)
    
    # 班级过滤
    if class_name:
        query = query.filter(Student.class_name == class_name)
    
    # 路线过滤
    if route_id is not None:
        query = query.filter(Student.route_id == route_id)
    
    # 状态过滤
    if status:
        query = query.filter(Student.status == status)
    
    # 关键词搜索（姓名、学号、家长电话）
    if keyword:
        query = query.filter(
            (Student.real_name.contains(keyword)) |
            (Student.student_code.contains(keyword)) |
            (Student.parent_phone.contains(keyword))
        )
    
    # 分页
    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个学生详情
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    # 权限控制：学校管理员只能查看本校学生
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if student.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法查看其他学校的学生"
            )
    
    return student


@router.post("/", response_model=StudentResponse)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新学生
    教育局管理员可以创建任意学校的学生，学校管理员只能创建本校学生
    """
    # 权限控制：学校管理员只能创建本校学生
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if student_data.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：只能创建本校的学生"
            )
    
    # 检查学号是否已存在
    if student_data.student_code:
        existing_student = db.query(Student).filter(
            Student.student_code == student_data.student_code
        ).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="学号已存在"
            )
    
    # 检查身份证号是否已存在
    if student_data.id_card:
        existing_id = db.query(Student).filter(
            Student.id_card == student_data.id_card
        ).first()
        if existing_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="身份证号已存在"
            )
    
    # 创建学生
    new_student = Student(**student_data.model_dump())
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新学生信息
    教育局管理员可以更新所有学生，学校管理员只能更新本校学生
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if student.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法修改其他学校的学生"
            )
    
    # 更新学生信息
    update_data = student_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    db.commit()
    db.refresh(student)
    
    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除学生
    教育局管理员可以删除任意学生，学校管理员只能删除本校学生
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="学生不存在"
        )
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        if student.school_id != current_user.school_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足：无法删除其他学校的学生"
            )
    
    db.delete(student)
    db.commit()
    
    return {"message": "学生删除成功"}


@router.get("/stats/overview")
def get_student_stats(
    school_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取学生统计信息
    """
    query = db.query(Student)
    
    # 权限控制
    if current_user.role == ROLES["SCHOOL_ADMIN"]:
        query = query.filter(Student.school_id == current_user.school_id)
    elif school_id is not None:
        query = query.filter(Student.school_id == school_id)
    
    # 统计总数
    total = query.count()
    active = query.filter(Student.status == "active").count()
    transferred = query.filter(Student.status == "transferred").count()
    graduated = query.filter(Student.status == "graduated").count()
    
    # 按路线统计
    route_stats = {}
    students_with_route = query.filter(Student.route_id.isnot(None)).all()
    for student in students_with_route:
        route_id = student.route_id
        if route_id not in route_stats:
            route_stats[route_id] = 0
        route_stats[route_id] += 1
    
    stats = {
        "total": total,
        "by_status": {
            "active": active,
            "transferred": transferred,
            "graduated": graduated
        },
        "by_route": route_stats
    }
    
    return stats
