"""
消息数据模型
=============

包含消息相关的请求和响应模型。
"""

from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class MessageCreate(BaseModel):
    """
    消息创建模型

    Attributes:
        title: 消息标题
        content: 消息内容
        message_type: 消息类型：parent(家长端)、driver(司机端)
        category_id: 消息分类ID
        receiver_id: 接收者ID
        extra_data: 额外数据
    """

    title: str = Field(..., max_length=200, description="消息标题")
    content: Optional[str] = Field(None, description="消息内容")
    message_type: str = Field(..., description="消息类型: parent/driver")
    category_id: Optional[int] = Field(None, description="消息分类ID")
    receiver_id: int = Field(..., description="接收者ID")
    extra_data: Optional[Any] = Field(None, description="额外数据")


class MessageUpdate(BaseModel):
    """
    消息更新模型

    Attributes:
        is_read: 是否已读
    """

    is_read: Optional[int] = Field(None, description="是否已读: 0-未读, 1-已读")


class MessageResponse(BaseModel):
    """
    消息响应模型

    Attributes:
        id: 消息ID
        title: 消息标题
        content: 消息内容
        message_type: 消息类型
        category_id: 消息分类ID
        category_name: 消息分类名称
        receiver_id: 接收者ID
        is_read: 是否已读
        read_time: 阅读时间
        extra_data: 额外数据
        created_at: 创建时间
        updated_at: 更新时间
    """

    id: int = Field(..., description="消息ID")
    title: str = Field(..., description="消息标题")
    content: Optional[str] = Field(None, description="消息内容")
    message_type: str = Field(..., description="消息类型")
    category_id: Optional[int] = Field(None, description="消息分类ID")
    category_name: Optional[str] = Field(None, description="消息分类名称")
    receiver_id: int = Field(..., description="接收者ID")
    is_read: int = Field(..., description="是否已读")
    read_time: Optional[datetime] = Field(None, description="阅读时间")
    extra_data: Optional[Any] = Field(None, description="额外数据")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    """
    消息列表响应模型

    Attributes:
        unread_count: 未读数量
        messages: 消息列表
    """

    unread_count: int = Field(0, description="未读数量")
    messages: list[MessageResponse] = Field([], description="消息列表")


class MessageCategoryResponse(BaseModel):
    """
    消息分类响应模型

    Attributes:
        id: 分类ID
        name: 分类名称
        code: 分类代码
        message_type: 消息类型
        description: 分类描述
        sort_order: 排序
        status: 状态
    """

    id: int = Field(..., description="分类ID")
    name: str = Field(..., description="分类名称")
    code: str = Field(..., description="分类代码")
    message_type: str = Field(..., description="消息类型")
    description: Optional[str] = Field(None, description="分类描述")
    sort_order: int = Field(0, description="排序")
    status: int = Field(1, description="状态")

    class Config:
        from_attributes = True


__all__ = [
    "MessageCreate",
    "MessageUpdate",
    "MessageResponse",
    "MessageListResponse",
    "MessageCategoryResponse",
]
