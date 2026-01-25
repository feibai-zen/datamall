from sqlalchemy import Column, Integer, String, DECIMAL, Date, TIMESTAMP, Boolean, BigInteger
from sqlalchemy.sql import func
from .database import Base


class ShareholderChangeRecord(Base):
    """
    股东持股变动记录表模型
    对应MySQL的shareholder_change_record表[1](@ref)
    """
    __tablename__ = "shareholder_change_record"

    # 主键与基本信息
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='记录ID，自增主键')
    stock_code = Column(String(20), index=True, comment='股票代码')
    stock_name = Column(String(50), comment='股票名称')
    latest_price = Column(DECIMAL(10, 2), comment='最新价')
    change_percent = Column(DECIMAL(5, 2), comment='涨跌幅(%)')

    # 股东信息
    shareholder_name = Column(String(260), index=True, comment='股东名称')
    change_type = Column(String(10), index=True, comment='持股变动类型-增减（如：减持、增持）')

    # 变动信息
    change_amount = Column(DECIMAL(20, 4), comment='持股变动数量（万股）')
    change_total_ratio = Column(DECIMAL(10, 6), comment='变动数量占总股本比例(%)')
    change_circulation_ratio = Column(DECIMAL(10, 6), comment='变动数量占流通股比例(%)')

    # 变动后持股情况
    after_total_holdings = Column(DECIMAL(20, 4), comment='变动后持股总数（万股）')
    after_total_ratio = Column(DECIMAL(10, 6), comment='变动后持股占总股本比例(%)')
    after_circulation_holdings = Column(DECIMAL(20, 4), comment='变动后持流通股数（万股）')
    after_circulation_ratio = Column(DECIMAL(10, 6), comment='变动后持股占流通股比例(%)')

    # 时间信息
    change_start_date = Column(Date, index=True, comment='变动开始日期')
    change_end_date = Column(Date, comment='变动截止日期')
    announcement_date = Column(Date, index=True, comment='公告日期')

    # 系统字段
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='记录创建时间')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='记录更新时间')
    is_deleted = Column(Boolean, default=False, comment='逻辑删除标记：0-正常，1-已删除')
