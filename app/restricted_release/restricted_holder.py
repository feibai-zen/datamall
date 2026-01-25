from fastapi import APIRouter
import akshare as ak
import pandas as pd
import numpy as np

router = APIRouter()


def convert_nan_to_none(value):
    """将NaN值转换为None"""
    if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
        return None
    return value


def convert_tuple_nan_to_none(data_tuple):
    """转换元组中的NaN值为None"""
    return tuple(convert_nan_to_none(item) for item in data_tuple)


# 解禁股东
# 目标地址: https://data.eastmoney.com/dxf/q/600000.html
# 描述: 东方财富网-数据中心-个股限售解禁-解禁股东
# 限量: 单次获取指定 symbol 的解禁批次数据
@router.get("/release_holder")
async def release_holder(symbol: str = "600000", date: str = "20200904"):
    ret = []

    try:
        restricted_release = ak.stock_restricted_release_stockholder_em(symbol, date)
        for row in restricted_release.itertuples(index=False):
            # 将行数据转换为元组
            values = tuple(convert_tuple_nan_to_none(row))
            print(values)
            ret.append(values)

        return {"message": ret}
    except Exception as e:
        print(e)
        return {"message": "no data found"}

# 解禁批次 —— 单次获取指定 symbol 的解禁批次数据
# 目标地址: https://data.eastmoney.com/dxf/q/600000.html
# 描述: 东方财富网-数据中心-个股限售解禁-解禁批次
# 限量: 单次获取指定 symbol 的解禁批次数据
@router.get("/release_batch")
async def release_batch(symbol: str = "600000", date: str = "20200904"):
    ret = []

    try:
        restricted_release = ak.stock_restricted_release_queue_em(symbol)
        for row in restricted_release.itertuples(index=False):
            # 将行数据转换为元组
            values = tuple(convert_tuple_nan_to_none(row))
            print(values)
            ret.append(values)

        return {"message": ret}
    except Exception as e:
        print(e)
        return {"message": "no data found"}