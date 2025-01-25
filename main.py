from typing import Optional, List
from fastapi import FastAPI, HTTPException, Path, Query, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import time
import random

# Initialize FastAPI app
app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add a variable to store the count
stored_count = 0

# --- Pydantic Models for Request/Response ---
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# --- Basic Routes ---
@app.get("/")
async def root(request: Request):
    """Serve the index.html template"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/customize")
async def customize(request: Request):
    """Serve the customize.html template"""
    return templates.TemplateResponse("customize.html", {"request": request})

@app.get("/hello/{name}")
async def say_hello(name: str):
    """Path parameter example"""
    return {"message": f"Hello, {name}!"}

# --- Query Parameters --- 
# Example /items/?skip=0&limit=10
@app.get("/items/")
async def read_items(
    start: int = Query(default=0, description="Number of items to start at"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of items to return")
):
    """Query parameters example with validation"""
    fake_items = [{"item_id": i} for i in range(start, start + limit)]
    return fake_items

# --- Request Body ---
# Example /items/
@app.post("/items/")
async def create_item(item: Item):
    """POST endpoint with request body validation using Pydantic"""
    return {"item": item, "message": "Item created successfully"}

# --- Path Parameters with Validation ---
# Example /items/42?q=test
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., ge=1, description="The ID of the item to retrieve"),
    q: Optional[str] = Query(None, max_length=50)
):
    """Path parameter with validation and optional query parameter"""
    if item_id == 42:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "q": q}

# --- Form Handling ---
@app.post("/submit")
async def handle_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    color: str = Form(...),
    interests: List[str] = Form(default=[])
):
    """Handle the form submission from index.html"""
    return {
        "status": "success",
        "data": {
            "name": name,
            "email": email,
            "message": message,
            "favorite_color": color,
            "interests": interests
        }
    }

# Add new route for the counter page
@app.get("/counter")
async def counter_page(request: Request):
    """Serve the counter.html template"""
    return templates.TemplateResponse("counter.html", {"request": request})

# Add routes for counter functionality
@app.get("/get_count")
async def get_count():
    """Return the current count"""
    return JSONResponse({"count": stored_count})

@app.post("/save_count")
async def save_count(data: dict):
    """Save the count to the server"""
    global stored_count
    stored_count = data.get("count", 0)
    return JSONResponse({
        "message": f"Count saved successfully: {stored_count}",
        "count": stored_count
    })

# Add new route for the counter page
@app.get("/cart")
async def cart_page(request: Request):
    """Serve the counter.html template"""
    return templates.TemplateResponse("cart.html", {"request": request})

@app.get("/api/price")
def get_price():
    """Return the price of an item"""
    # wait a random amount of time between 1 and 5 seconds
    time.sleep(random.randint(1, 5))
    return JSONResponse({"price": 10.99})

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
