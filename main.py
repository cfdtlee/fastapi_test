from fastapi import FastAPI

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