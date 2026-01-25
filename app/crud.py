from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import date, datetime, timedelta
from typing import List, Optional
from . import models, schemas


def create_shareholder_change_record(
        db: Session,
        record: schemas.ShareholderChangeRecordCreate
) -> models.ShareholderChangeRecord:
    """
    创建股东持股变动记录[5](@ref)
    """
    db_record = models.ShareholderChangeRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_record_by_id(
        db: Session,
        record_id: int
) -> Optional[models.ShareholderChangeRecord]:
    """
    根据ID查询记录[5](@ref)
    """
    return db.query(models.ShareholderChangeRecord) \
        .filter(models.ShareholderChangeRecord.id == record_id) \
        .filter(models.ShareholderChangeRecord.is_deleted == False) \
        .first()


def get_records_by_stock_code(
        db: Session,
        stock_code: str,
        skip: int = 0,
        limit: int = 100
) -> List[models.ShareholderChangeRecord]:
    """
    按照股票代码查询记录[1](@ref)
    """
    return db.query(models.ShareholderChangeRecord) \
        .filter(models.ShareholderChangeRecord.stock_code == stock_code) \
        .filter(models.ShareholderChangeRecord.is_deleted == False) \
        .order_by(models.ShareholderChangeRecord.announcement_date.desc()) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_records_by_stock_name(
        db: Session,
        stock_name: str,
        skip: int = 0,
        limit: int = 100
) -> List[models.ShareholderChangeRecord]:
    """
    按照股票名称查询记录
    """
    return db.query(models.ShareholderChangeRecord) \
        .filter(models.ShareholderChangeRecord.stock_name.like(f"%{stock_name}%")) \
        .filter(models.ShareholderChangeRecord.is_deleted == False) \
        .order_by(models.ShareholderChangeRecord.announcement_date.desc()) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_records_by_announcement_date(
        db: Session,
        announcement_date: date,
        skip: int = 0,
        limit: int = 100
) -> List[models.ShareholderChangeRecord]:
    """
    按照公告日期查询所有变动记录
    """
    return db.query(models.ShareholderChangeRecord) \
        .filter(models.ShareholderChangeRecord.announcement_date == announcement_date) \
        .filter(models.ShareholderChangeRecord.is_deleted == False) \
        .order_by(models.ShareholderChangeRecord.stock_code) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_records_by_change_date_range(
        db: Session,
        days: int = 60,
        skip: int = 0,
        limit: int = 100
) -> List[models.ShareholderChangeRecord]:
    """
    查询变动开始日期在今天之后，且小于指定天数的记录
    """
    today = date.today()
    future_date = today + timedelta(days=days)

    return db.query(models.ShareholderChangeRecord) \
        .filter(
        and_(
            models.ShareholderChangeRecord.change_start_date >= today,
            models.ShareholderChangeRecord.change_start_date <= future_date,
            models.ShareholderChangeRecord.is_deleted == False
        )
    ) \
        .order_by(models.ShareholderChangeRecord.change_start_date.asc()) \
        .offset(skip) \
        .limit(limit) \
        .all()


def update_shareholder_change_record(
        db: Session,
        record_id: int,
        record_update: schemas.ShareholderChangeRecordUpdate
) -> Optional[models.ShareholderChangeRecord]:
    """
    更新股东持股变动记录[1](@ref)
    """
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return None

    update_data = record_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)

    db.commit()
    db.refresh(db_record)
    return db_record


def delete_shareholder_change_record(
        db: Session,
        record_id: int,
        soft_delete: bool = True
) -> bool:
    """
    删除记录（支持逻辑删除）[1](@ref)
    """
    db_record = get_record_by_id(db, record_id)
    if not db_record:
        return False

    if soft_delete:
        db_record.is_deleted = True
    else:
        db.delete(db_record)

    db.commit()
    return True


def search_records(
        db: Session,
        query: schemas.ShareholderChangeRecordQuery
) -> List[models.ShareholderChangeRecord]:
    """
    综合查询方法
    """
    filters = [models.ShareholderChangeRecord.is_deleted == False]

    if query.stock_code:
        filters.append(models.ShareholderChangeRecord.stock_code == query.stock_code)

    if query.stock_name:
        filters.append(models.ShareholderChangeRecord.stock_name.like(f"%{query.stock_name}%"))

    if query.announcement_date:
        filters.append(models.ShareholderChangeRecord.announcement_date == query.announcement_date)

    if query.change_start_date_from:
        filters.append(models.ShareholderChangeRecord.change_start_date >= query.change_start_date_from)

    return db.query(models.ShareholderChangeRecord) \
        .filter(and_(*filters)) \
        .order_by(models.ShareholderChangeRecord.announcement_date.desc()) \
        .offset(query.skip) \
        .limit(query.limit) \
        .all()
