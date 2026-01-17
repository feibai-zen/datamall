import pandas as pd
import pymysql
import db_config

def get_db_connection():
    try:
        # 连接数据库
        mydb = pymysql.connect(
            host=db_config.host,
            user=db_config.user,
            password=db_config.password,
            database=db_config.database
        )
        return mydb
    except pymysql.connect.Error as err:
        print(f"数据库连接或操作出错: {err}")
    finally:
        # 关闭连接
        if 'mydb' in locals():
            mydb.close()

def get_db_cursor():
    try:
        return get_db_connection().cursor()
    except pymysql.connect.Error as err:
        print(f"数据库连接或操作出错: {err}")
    finally:
        # 关闭连接
        if 'mycursor' in locals():
            mycursor.close()