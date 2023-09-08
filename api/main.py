from fastapi import FastAPI
from models import messageModel
from fastapi import HTTPException, status

import random

app = FastAPI()


@app.get("/", response_model=messageModel) 
async def get_route():
  
  try:   
    return {"message": "Hello!"}
  
  except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}."
    )


@app.get("/deadpeople", response_model=messageModel) 
async def get_dead_route():
  people = ["Jacques Chirac", "Alan Turing", "Napoleon"]

  try:   
    return {"message": f"Hey, it is me, {random.choice(people)}!"}
  
  except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}."
    )


@app.post("/", response_model=messageModel) 
async def post_route(obj_in: messageModel):  

  try:
    return_object = obj_in.model_dump()
    original_message = return_object["message"]
    return_object["message"] = f"I heard: {original_message}"
    return return_object
  
  except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}."
    )