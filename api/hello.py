from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/hello")
async def hello_world():
    return {"message": "Hello World from API"}


@router.get("/hello/{name}")
async def say_hello(name: str, times: Optional[int] = 1):
    """
    打招呼接口

    - **name**: 用户名
    - **times**: 重复次数（可选，默认为1）
    """
    return {
        "message": f"Hello {name}!" * times,
        "name": name,
        "times": times
    }


# 带查询参数的版本  http://localhost:8000/api/greet?name=liyuanlong
@router.get("/greet")
async def greet(name: str = "World"):
    return {"greeting": f"Hello {name}!"}