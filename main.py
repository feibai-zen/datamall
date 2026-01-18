
from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title="Hello World API",
    description="一个简单的 Hello World API 演示",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
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


# 带查询参数的版本
@app.get("/greet")
async def greet(name: str = "World"):
    return {"greeting": f"Hello {name}!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=9001, reload=True)
