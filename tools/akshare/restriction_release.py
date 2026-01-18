import pandas as pd
import akshare as ak
import pymysql
import numpy as np
from datetime import date, timedelta

# 解禁详情

host = '8.153.196.139'
user = 'root'
password = '286072955b063d1d'
database = 'zen'


def convert_nan_to_none(value):
    """将NaN值转换为None"""
    if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
        return None
    return value


def convert_tuple_nan_to_none(data_tuple):
    """转换元组中的NaN值为None"""
    return tuple(convert_nan_to_none(item) for item in data_tuple)


def insert_dataframe_to_mysql(fetch_date, need_total, df, table_name, table_columns):
    """
    将DataFrame数据逐行插入到MySQL数据库
    """

    try:
        # 连接数据库
        mydb = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # 创建游标对象
        mycursor = mydb.cursor()

        # TRUNCATE会重置自增ID，更快且自动提交事务
        sql = "TRUNCATE TABLE restricted_shares_release_detail"
        mycursor.execute(sql)
        mydb.commit()
        print(f"成功清空表 restricted_shares_release_detail")

        # 获取列名
        columns = list(df.columns)
        placeholders = ', '.join(['%s'] * len(columns))

        # 准备SQL语句
        sql = f"INSERT INTO {table_name} ({table_columns}) VALUES ({placeholders})"

        # 逐行插入数据
        success_count = 0
        error_count = 0

        for row in df.itertuples(index=False):
            try:
                # 将行数据转换为元组
                values = tuple(convert_tuple_nan_to_none(row))
                # if need_total == False and fetch_date is not None and values[4].strftime("%Y-%m-%d") == fetch_date:
                #     continue

                mycursor.execute(sql, values)
                success_count += 1
                # 每100行提交一次，平衡性能和数据安全
                if success_count % 100 == 0:
                    mydb.commit()
            except pymysql.connect.Error as err:
                print(f"插入数据时出错: {err}")
                error_count += 1
                continue

        # 最终提交
        mydb.commit()

        print(f"日期:{fetch_date}, 数据插入完成！成功: {success_count}条，失败: {error_count}条")

    except pymysql.connect.Error as err:
        print(f"数据库连接或操作出错: {err}")

    finally:
        # 关闭连接
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()


if __name__ == '__main__':
    current_date = date.today()
    days_ago = current_date - timedelta(days=1)
    fetch_date = days_ago.strftime("%Y-%m-%d")
    table_cols = 'stock_code,stock_name,release_time,restricted_share_type,release_quantity,actual_release_quantity,actual_release_market_value,proportion_of_released_market_value,closing_price_before_release_day,price_change_rate_20_days_before_release,price_change_rate_20_days_after_release'

    print(f"==============DAILY BEGIN: {fetch_date}=====================")
    df = ak.stock_restricted_release_detail_em(start_date="19000101", end_date="30001231")

    # pick up from the second column in the df
    insert_dataframe_to_mysql(fetch_date=fetch_date, need_total=False, df=df.iloc[:, 1:],
                              table_name='restricted_shares_release_detail',
                              table_columns=table_cols)
    print(f"==============DAILY END: {fetch_date}=======================")
