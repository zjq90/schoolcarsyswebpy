"""
政策数据模型
定义教育局发布的政策信息
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Policy(Base):
    """
    政策表
    存储教育局发布的政策信息
    """
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True, comment="政策ID，主键")
    policy_code = Column(String(50), unique=True, index=True, comment="政策编码")
    title = Column(String(200), nullable=False, comment="政策标题")
    content = Column(Text, nullable=False, comment="政策内容")
    policy_type = Column(String(50), default="notice", comment="政策类型：notice(通知) / regulation(规定) / guidance(指导)")
    publisher_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="发布人ID（教育局管理员）")
    publish_date = Column(Date, comment="发布日期")
    effective_date = Column(Date, comment="生效日期")
    expiry_date = Column(Date, comment="失效日期")
    is_published = Column(Boolean, default=False, comment="是否已发布")
    is_top = Column(Boolean, default=False, comment="是否置顶")
    attachment_path = Column(String(500), comment="附件路径")
    view_count = Column(Integer, default=0, comment="浏览次数")
    status = Column(String(20), default="draft", comment="状态：draft(草稿) / published(已发布) / expired(已过期)")
    remarks = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系定义
    publisher = relationship("User")

    def __repr__(self):
        return f"<Policy(id={self.id}, title={self.title})>"
