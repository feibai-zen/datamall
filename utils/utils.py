
import pandas as pd
import numpy as np

def convert_nan_to_none(value):
    """将NaN值转换为None"""
    if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
        return None
    return value

def convert_tuple_nan_to_none(data_tuple):
    """转换元组中的NaN值为None"""
    return tuple(convert_nan_to_none(item) for item in data_tuple)