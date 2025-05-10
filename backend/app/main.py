from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, student, teacher, admin

app = FastAPI(
    title="简易课程评价系统API",
    description="用于课程评价系统的后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应当限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含各模块路由，添加/api前缀
app.include_router(auth.router, prefix="/api")
app.include_router(student.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "欢迎使用简易课程评价系统API"}

# 如果直接运行此文件
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 