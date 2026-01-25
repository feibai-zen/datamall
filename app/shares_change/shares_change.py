from datetime import date
from typing import List, Optional

from fastapi import Depends, HTTPException, Query, status, APIRouter
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post(
    "/records/",
    response_model=schemas.ShareholderChangeRecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建股东持股变动记录",
    tags=["记录管理"]
)
def create_record(
    record: schemas.ShareholderChangeRecordCreate,
    db: Session = Depends(get_db)
):
    """
    创建新的股东持股变动记录
    """
    return crud.create_shareholder_change_record(db, record)

@router.get(
    "/records/stock-code/{stock_code}",
    response_model=List[schemas.ShareholderChangeRecordResponse],
    summary="按照股票代码查询记录",
    tags=["查询接口"]
)
def read_records_by_stock_code(
    stock_code: str,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """
    根据股票代码查询股东持股变动记录
    - **stock_code**: 股票代码（如：000001.SZ）
    - **skip**: 分页偏移量
    - **limit**: 每页记录数
    """
    records = crud.get_records_by_stock_code(db, stock_code, skip, limit)
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到股票代码为 {stock_code} 的记录"
        )
    return records

@router.get(
    "/records/stock-name/{stock_name}",
    response_model=List[schemas.ShareholderChangeRecordResponse],
    summary="按照股票名称查询记录",
    tags=["查询接口"]
)
def read_records_by_stock_name(
    stock_name: str,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """
    根据股票名称查询股东持股变动记录（支持模糊查询）
    - **stock_name**: 股票名称（支持模糊匹配）
    - **skip**: 分页偏移量
    - **limit**: 每页记录数
    """
    records = crud.get_records_by_stock_name(db, stock_name, skip, limit)
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到股票名称包含 '{stock_name}' 的记录"
        )
    return records

@router.get(
    "/records/announcement-date/{announcement_date}",
    response_model=List[schemas.ShareholderChangeRecordResponse],
    summary="按照公告日期查询记录",
    tags=["查询接口"]
)
def read_records_by_announcement_date(
    announcement_date: date,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """
    根据公告日期查询所有变动记录
    - **announcement_date**: 公告日期（格式：YYYY-MM-DD）
    - **skip**: 分页偏移量
    - **limit**: 每页记录数
    """
    records = crud.get_records_by_announcement_date(db, announcement_date, skip, limit)
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到公告日期为 {announcement_date} 的记录"
        )
    return records

@router.get(
    "/records/upcoming-changes/",
    response_model=List[schemas.ShareholderChangeRecordResponse],
    summary="查询近期变动记录",
    tags=["查询接口"]
)
def read_upcoming_changes(
    days: int = Query(60, ge=1, le=365, description="未来天数范围"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """
    查询变动开始日期在今天之后，且小于指定天数的记录
    - **days**: 未来天数范围（默认60天）
    - **skip**: 分页偏移量
    - **limit**: 每页记录数
    """
    records = crud.get_records_by_change_date_range(db, days, skip, limit)
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到未来{days}天内的变动记录"
        )
    return records

@router.get(
    "/records/search/",
    response_model=List[schemas.ShareholderChangeRecordResponse],
    summary="综合查询记录",
    tags=["查询接口"]
)
def search_records(
    stock_code: Optional[str] = Query(None, description="股票代码"),
    stock_name: Optional[str] = Query(None, description="股票名称"),
    announcement_date: Optional[date] = Query(None, description="公告日期"),
    change_start_date_from: Optional[date] = Query(None, description="变动开始日期起始"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """
    综合查询股东持股变动记录，支持多条件组合查询
    """
    query = schemas.ShareholderChangeRecordQuery(
        stock_code=stock_code,
        stock_name=stock_name,
        announcement_date=announcement_date,
        change_start_date_from=change_start_date_from,
        skip=skip,
        limit=limit
    )
    records = crud.search_records(db, query)
    return records

@router.get(
    "/records/{record_id}",
    response_model=schemas.ShareholderChangeRecordResponse,
    summary="根据ID查询记录",
    tags=["记录管理"]
)
def read_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    根据记录ID查询单个股东持股变动记录
    """
    record = crud.get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到ID为 {record_id} 的记录"
        )
    return record

@router.put(
    "/records/{record_id}",
    response_model=schemas.ShareholderChangeRecordResponse,
    summary="更新记录",
    tags=["记录管理"]
)
def update_record(
    record_id: int,
    record_update: schemas.ShareholderChangeRecordUpdate,
    db: Session = Depends(get_db)
):
    """
    更新股东持股变动记录
    """
    record = crud.update_shareholder_change_record(db, record_id, record_update)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到ID为 {record_id} 的记录"
        )
    return record

@router.delete(
    "/records/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除记录",
    tags=["记录管理"]
)
def delete_record(
    record_id: int,
    soft_delete: bool = Query(True, description="是否逻辑删除"),
    db: Session = Depends(get_db)
):
    """
    删除股东持股变动记录（支持逻辑删除和物理删除）
    - **soft_delete**: True为逻辑删除（默认），False为物理删除
    """
    success = crud.delete_shareholder_change_record(db, record_id, soft_delete)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到ID为 {record_id} 的记录"
        )