import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

app = FastAPI()

base_dir = Path(__file__).parent
static_dir = os.path.join(base_dir, "static")

# Проверяем существует ли директория
if not os.path.exists(static_dir):
    raise Exception(f"Static directory not found at: {static_dir}")

# Отдаём статику (Mini App)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

products = [
    {"id": 1, "name": "Кроссовки Nike Air Max", "price": 5990, "image": "/static/nike.jpg"},
    {"id": 2, "name": "Кеды Converse", "price": 3990, "image": "/static/converse.jpg"}
]

# API для получения товаров
@app.get("/api/products")
async def get_products():
    return JSONResponse(products)

# Главная страница (Mini App)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(), status_code=200)

    