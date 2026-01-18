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


@router.get("/release_stockholder")
async def hello_world(symbol: str = "600000", date: str = "20200904"):
    restricted_release = ak.stock_restricted_release_stockholder_em(symbol="600000", date="20200904")

    ret = []
    for row in restricted_release.itertuples(index=False):
        try:
            # 将行数据转换为元组
            values = tuple(convert_tuple_nan_to_none(row))
            print(values)
            ret.append(values)
        except Exception as e:
            print(e)
            continue

    return {"message": ret}
