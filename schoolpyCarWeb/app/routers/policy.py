"""
政策管理路由模块
处理政策的增删改查功能（教育局管理员专用）
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.policy import Policy
from app.models.user import User
from app.schemas.policy import PolicyCreate, PolicyResponse, PolicyUpdate
from app.routers.auth import get_current_user, get_current_user_with_permission
from app.config import ROLES

router = APIRouter(prefix="/api/policies", tags=["政策管理"])


@router.get("/", response_model=List[PolicyResponse])
def get_policies(
    skip: int = 0,
    limit: int = 100,
    policy_type: Optional[str] = None,
    status: Optional[str] = None,
    is_published: Optional[bool] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取政策列表
    所有人都可以查看已发布的政策，教育局管理员可以查看所有政策
    """
    query = db.query(Policy)
    
    # 权限控制：非教育局管理员只能看到已发布的政策
    if current_user.role != ROLES["EDUCATION_BUREAU"]:
        query = query.filter(Policy.is_published == True)
    
    # 类型过滤
    if policy_type:
        query = query.filter(Policy.policy_type == policy_type)
    
    # 状态过滤
    if status:
        query = query.filter(Policy.status == status)
    
    # 发布状态过滤
    if is_published is not None:
        query = query.filter(Policy.is_published == is_published)
    
    # 关键词搜索（标题、内容）
    if keyword:
        query = query.filter(
            (Policy.title.contains(keyword)) |
            (Policy.content.contains(keyword))
        )
    
    # 排序：置顶优先，然后按发布时间倒序
    query = query.order_by(Policy.is_top.desc(), Policy.publish_date.desc(), Policy.created_at.desc())
    
    # 分页
    policies = query.offset(skip).limit(limit).all()
    return policies


@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个政策详情
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    
    # 权限控制：非教育局管理员只能查看已发布的政策
    if current_user.role != ROLES["EDUCATION_BUREAU"]:
        if not policy.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="政策不存在"
            )
    
    # 增加浏览次数（只有教育局管理员以外的用户浏览才增加）
    if current_user.role != ROLES["EDUCATION_BUREAU"]:
        policy.view_count += 1
        db.commit()
        db.refresh(policy)
    
    return policy


@router.post("/", response_model=PolicyResponse)
def create_policy(
    policy_data: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    创建新政策
    只有教育局管理员可以创建政策
    """
    # 检查政策编码是否已存在
    if policy_data.policy_code:
        existing_policy = db.query(Policy).filter(
            Policy.policy_code == policy_data.policy_code
        ).first()
        if existing_policy:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="政策编码已存在"
            )
    
    # 设置发布人为当前用户
    policy_data.publisher_id = current_user.id
    
    # 创建政策
    new_policy = Policy(**policy_data.model_dump())
    
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    
    return new_policy


@router.put("/{policy_id}", response_model=PolicyResponse)
def update_policy(
    policy_id: int,
    policy_data: PolicyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    更新政策信息
    只有教育局管理员可以更新政策
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    
    # 更新政策信息
    update_data = policy_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(policy, key, value)
    
    db.commit()
    db.refresh(policy)
    
    return policy


@router.delete("/{policy_id}")
def delete_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    删除政策
    只有教育局管理员可以删除政策
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    
    db.delete(policy)
    db.commit()
    
    return {"message": "政策删除成功"}


@router.put("/{policy_id}/publish")
def publish_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    发布政策
    只有教育局管理员可以发布政策
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    
    from datetime import date
    policy.is_published = True
    policy.status = "published"
    if not policy.publish_date:
        policy.publish_date = date.today()
    
    db.commit()
    
    return {"message": "政策发布成功"}


@router.put("/{policy_id}/top")
def toggle_policy_top(
    policy_id: int,
    is_top: bool = Query(True, description="是否置顶"),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_with_permission(required_roles=[ROLES["EDUCATION_BUREAU"]])
    )
):
    """
    设置/取消政策置顶
    只有教育局管理员可以操作
    """
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在"
        )
    
    policy.is_top = is_top
    db.commit()
    
    return {"message": f"政策{'已置顶' if is_top else '已取消置顶'}"}
