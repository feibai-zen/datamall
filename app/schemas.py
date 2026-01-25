from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class ShareholderChangeRecordBase(BaseModel):
    """基础数据模型"""
    stock_code: Optional[str] = Field(None, max_length=20, description='股票代码')
    stock_name: Optional[str] = Field(None, max_length=50, description='股票名称')
    latest_price: Optional[Decimal] = Field(None, description='最新价')
    change_percent: Optional[Decimal] = Field(None, description='涨跌幅(%)')
    shareholder_name: Optional[str] = Field(None, max_length=260, description='股东名称')
    change_type: Optional[str] = Field(None, max_length=10, description='持股变动类型')
    change_amount: Optional[Decimal] = Field(None, description='持股变动数量（万股）')
    change_total_ratio: Optional[Decimal] = Field(None, description='变动数量占总股本比例(%)')
    change_circulation_ratio: Optional[Decimal] = Field(None, description='变动数量占流通股比例(%)')
    after_total_holdings: Optional[Decimal] = Field(None, description='变动后持股总数（万股）')
    after_total_ratio: Optional[Decimal] = Field(None, description='变动后持股占总股本比例(%)')
    after_circulation_holdings: Optional[Decimal] = Field(None, description='变动后持流通股数（万股）')
    after_circulation_ratio: Optional[Decimal] = Field(None, description='变动后持股占流通股比例(%)')
    change_start_date: Optional[date] = Field(None, description='变动开始日期')
    change_end_date: Optional[date] = Field(None, description='变动截止日期')
    announcement_date: Optional[date] = Field(None, description='公告日期')


class ShareholderChangeRecordCreate(ShareholderChangeRecordBase):
    """创建记录请求模型[3](@ref)"""
    stock_code: str = Field(..., max_length=20, description='股票代码')
    shareholder_name: str = Field(..., max_length=260, description='股东名称')
    change_type: str = Field(..., max_length=10, description='持股变动类型')


class ShareholderChangeRecordUpdate(ShareholderChangeRecordBase):
    """更新记录请求模型"""
    pass


class ShareholderChangeRecordResponse(ShareholderChangeRecordBase):
    """查询响应模型[3](@ref)[5](@ref)"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True  # 启用ORM模式，允许从SQLAlchemy对象转换[3](@ref)[5](@ref)


class ShareholderChangeRecordQuery(BaseModel):
    """查询参数模型"""
    stock_code: Optional[str] = None
    stock_name: Optional[str] = None
    announcement_date: Optional[date] = None
    change_start_date_from: Optional[date] = None
    skip: int = 0
    limit: int = 100
