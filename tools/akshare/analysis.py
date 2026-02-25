import pandas as pd
import akshare as ak
import pymysql
import numpy as np
from datetime import date, timedelta

# 股东增减持——增量拉取/全量拉取
host = '8.153.196.139'
user = 'root'
password = '286072955b063d1d'
database = 'zen'

select_sql = "select * from restricted_shares_release_detail where release_time BETWEEN CURDATE() AND (CURDATE() + INTERVAL 7 DAY) order by actual_release_market_value desc, release_time desc,stock_code"


def read_data_from_mysql():
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
        mycursor.execute(select_sql)
        ret = mycursor.fetchall()
        print(f"成功清空股东增减持表 {ret}\n")
    except pymysql.connect.Error as err:
        print(f"数据库连接或操作出错: {err}\n")
    finally:
        # 关闭连接
        if 'mycursor' in locals():
            mycursor.close()
        if 'mydb' in locals():
            mydb.close()


if __name__ == '__main__':
    current_date = date.today()
    days_ago = current_date - timedelta(days=1)
    # print(f"==============DAILY BEGIN: {fetch_date}=====================\n")
    # df = stock_ggcg_em_df = ak.stock_ggcg_em(symbol="全部")  # symbol="全部"; choice of {"全部", "股东增持", "股东减持"}  # 读取数据
    read_data_from_mysql()
    # print(f"==============DAILY END: {fetch_date}=======================\n")
