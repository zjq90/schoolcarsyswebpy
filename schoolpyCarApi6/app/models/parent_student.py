"""
家长学生关联模型
=================

家长与学生的关联表，实现多对多关系。
一个家长可以关联多个学生，一个学生可以有多个家长。
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ParentStudent(Base):
    """
    家长与学生关联表

    Attributes:
        id: 关联ID，主键
        parent_id: 家长ID，外键
        student_id: 学生ID，外键
        relation: 与学生的关系：父亲、母亲、其他
        status: 状态：1-已绑定，0-已解绑
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "parent_student"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False, comment="家长ID")
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, comment="学生ID")
    relation = Column(String(20), nullable=True, comment="与学生的关系: 父亲/母亲/其他")
    status = Column(Integer, default=1, comment="状态: 1-已绑定, 0-已解绑")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    parent = relationship("Parent", backref="student_relations")
    student = relationship("Student", backref="parent_relations")

    def __repr__(self):
        return f"<ParentStudent(id={self.id}, parent_id={self.parent_id}, student_id={self.student_id})>"
