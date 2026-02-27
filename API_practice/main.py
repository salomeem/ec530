# FastAPI reads paths liner my line, is value has same path it will be overriden with earlier one
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


# to initialize: uvicorn main:app --reload

app = FastAPI()

# default, returns for root link (localhost:8000/)
# adding /docs at the end will get you a Swagger UI representation of your endpoints
# adding /redoc gives redoc representation
@app.get("/")
def read_root():
    return {"Hello": "World"}

# new endpoint, responds to (localhost:8000/items/#?q=value)
# ? signifies beginning of query
# {} makes value dynamic
@app.get("/items/{item_id}")

# in function specify type
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

#################################
@app.get("/blog")
# query params specified in function, not endpoint
def index(limit: int, published: bool, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
       return {"data": f"{limit} unpublished blogs from the db"} 
    
class Blog(BaseModel):
    pass
    title:str
    body: str
    published: Optional[bool] = None
        
@app.post("/blog")
def create_blog(blog:Blog):
    # use dot notation to access base model;
    return {"data": f"Blog is created with title as {blog.title}"}
    
@app.get("/blog/{id}/comments")
# automatically identifies the first input as a path parameter
# knows the rest are query parameters
def comments(id, limit=10):
    return id
    # return {"data": {'1','2'}}

