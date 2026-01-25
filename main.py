from fastapi import FastAPI
from app import hello
from app.restricted_release import restricted_holder

app = FastAPI(
    title="Hello World API",
    description="一个简单的 Hello World API 演示",
    version="1.0.0"
)

# 包含API路由
app.include_router(hello.router, prefix="/app", tags=["hello"])
app.include_router(restricted_holder.router, prefix="/restricted", tags=["hello"])

@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    # 启动服务器，端口可自定义
    uvicorn.run(app, host="0.0.0.0", port=8000)
