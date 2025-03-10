from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str

app = FastAPI()

# 添加 CORS 中间件，允许前端访问
frontend_url = os.environ.get("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items = []

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/process-url")
def process_url(request: URLRequest):
    # 这里添加您的 URL 处理逻辑
    url = request.url
    # 示例：返回 URL 的长度和是否包含 https
    return {
        "url": url,
        "length": len(url),
        "is_https": url.startswith("https://"),
        "status": "processed"
    }

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return {"message": "Item created"}

@app.get("/items")
def get_items():
    return {"items": items}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item": items[item_id]}

# 添加这段代码以便在本地和生产环境都能运行
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)