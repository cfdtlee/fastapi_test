from fastapi import FastAPI
import os

app = FastAPI()

items = []

@app.get("/")
def read_root():
    return {"message": "Hello World"}

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