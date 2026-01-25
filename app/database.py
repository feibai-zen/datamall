from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 数据库连接字符串[1](@ref)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/shareholder_db")

# 创建数据库引擎[1](@ref)[5](@ref)
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # 连接池大小
    max_overflow=20,        # 连接池最大溢出数
    pool_recycle=3600,      # 连接回收时间（秒）
    pool_pre_ping=True,     # 预检查连接是否有效
    echo=True               # 开发环境开启SQL日志
)

# 创建会话工厂[1](@ref)[5](@ref)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基类[1](@ref)[3](@ref)
Base = declarative_base()

# 依赖注入函数，用于获取数据库会话[1](@ref)[5](@ref)
def get_db():
    """
    提供数据库会话的依赖注入函数
    每个请求独立会话，请求结束后自动关闭[5](@ref)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
