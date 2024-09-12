from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义Pydantic模型用于请求验证
class Item(BaseModel):
    name: str
    price: float

# 定义依赖项
async def get_db():
    # 这里应该是实际的数据库连接逻辑
    db = {"items": []}
    yield db

# 定义一个简单的中间件
@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Process-Time"] = "0.1"
    return response

# 路由处理函数
@app.post("/items/", response_model=Item)
async def create_item(item: Item, db: dict = Depends(get_db)):
    db["items"].append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items(db: dict = Depends(get_db)):
    return db["items"]

# 异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"detail": exc.detail}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
