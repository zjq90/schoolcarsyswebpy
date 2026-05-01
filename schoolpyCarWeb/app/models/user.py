"""
用户数据模型
定义系统用户（教育局、学校管理员）的数据结构
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    用户表
    存储系统用户信息，包括教育局管理员和学校管理员
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="用户ID，主键")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码（加密存储）")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    role = Column(String(50), nullable=False, comment="角色：education_bureau(教育局) / school_admin(学校管理员)")
    phone = Column(String(20), comment="联系电话")
    email = Column(String(100), comment="邮箱")
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True, comment="所属学校ID（学校管理员必填，教育局可为空）")
    is_active = Column(Boolean, default=True, comment="是否启用")
    last_login = Column(DateTime, comment="最后登录时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    school = relationship("School", back_populates="admins")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
