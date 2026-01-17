import pandas as pd
import akshare as ak
import pymysql
import numpy as np
from datetime import date, timedelta

host = '8.153.196.139'
user = 'root'
password = '286072955b063d1d'
database = 'zen'
table = 'shareholder_change_record'


def convert_nan_to_none(value):
    """将NaN值转换为None"""
    if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
        return None
    return value

def convert_tuple_nan_to_none(data_tuple):
    """转换元组中的NaN值为None"""
    return tuple(convert_nan_to_none(item) for item in data_tuple)


def insert_dataframe_to_mysql(df, table_name, table_columns):
    """
    将DataFrame数据逐行插入到MySQL数据库
    """

    current_date = date.today()
    days_ago = current_date - timedelta(days=1)
    fetch_date = days_ago.strftime("%Y-%m-%d")
    print("==============DAILY BEGIN: {fetch_date}=====================")
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

        # 获取列名
        columns = list(df.columns)
        placeholders = ', '.join(['%s'] * len(columns))

        # 准备SQL语句
        sql = f"INSERT INTO {table} ({table_columns}) VALUES ({placeholders})"

        # 逐行插入数据
        success_count = 0
        error_count = 0

        for row in df.itertuples(index=False):
            try:
                # 将行数据转换为元组
                values = tuple(convert_tuple_nan_to_none(row))
                if fetch_date is not None and values[-1].strftime("%Y-%m-%d") != fetch_date:
                   continue

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
    print("==============DAILY END: {fetch_date}=====================")


if __name__ == '__main__':
    df = stock_ggcg_em_df = ak.stock_ggcg_em(symbol="全部")   # symbol="全部"; choice of {"全部", "股东增持", "股东减持"}  # 读取数据
    insert_dataframe_to_mysql(df=df, table_name='shareholder_change_record',table_columns='stock_code,stock_name,latest_price,change_percent,shareholder_name,change_type,change_amount,change_total_ratio,change_circulation_ratio,after_total_holdings,after_total_ratio,after_circulation_holdings,after_circulation_ratio,change_start_date,change_end_date,announcement_date')
