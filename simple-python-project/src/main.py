from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List

# Initialize FastAPI app
app = FastAPI(
    title="Learn FastAPI",
    description="A simple API to learn FastAPI concepts",
    version="1.0.0"
)

# Pydantic models for request/response
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool

# In-memory storage
items_db = {}
item_id_counter = 1

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to FastAPI Learning API!"}

@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """
    Create a new item.
    
    Args:
        item (Item): The item data to create
        
    Returns:
        ItemResponse: The created item with its ID
    """
    global item_id_counter
    item_dict = item.dict()
    item_dict["id"] = item_id_counter
    items_db[item_id_counter] = item_dict
    item_id_counter += 1
    return item_dict

@app.get("/items/", response_model=List[ItemResponse])
async def list_items():
    """
    List all items.
    
    Returns:
        List[ItemResponse]: List of all items
    """
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """
    Get a specific item by ID.
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        ItemResponse: The requested item
        
    Raises:
        HTTPException: If the item is not found
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return items_db[item_id]

# @app.get("/")
# def read_root():
#     return "Hello world"

#create a post endpoint called postAplication() retururn "message": "Application submitted successfully"
@app.post("/application")
def post_application():
    return {"message": "Application submitted successfully"}


#Create another POST request called applyForCandidate() -> /application/{candidate_id}
#return "Application for candidateID: 122 successfully submitted"

@app.post("/apply")
def get_application():
    return {
        "status": "success",
        "message": "Application for "+candidate_id +" successfully submitted",

    }

@app.post("/apply/{candidate_id}")
def get_application(candidate_id: str):
    return {
        "status": "success",
        "message": "Application for "+candidate_id +" successfully submitted",

    }

#add a get request to get the application for a candidate it should support query parameters like company name = str
#if query parameter is provided return only the applications for that company
#if query parameter is not provided return all applications
@app.get("/applications")
def get_applications(company_name: str = Query(None, discription = "it can be null" ), candidate_email: str = Query(None, discription = "it can be null" )):
    if company_name:
        return {
            "status": "success",
            "message": "Applications for "+company_name +" successfully retrieved",
        }
    else:
        return {
            "status": "success",
            "message": "All applications successfully retrieved",
        }
