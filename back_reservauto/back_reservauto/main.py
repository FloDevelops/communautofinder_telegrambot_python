import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
# from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from back_reservauto.database import engine
from back_reservauto import models
from back_reservauto.routers.api import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)



def dev():
    '''Launch by `poetry run start` at the root of the project'''
    uvicorn.run('back_reservauto.main:app', host='0.0.0.0', port=8000, reload=True)


# Users
# List Users:

# GET /users
# Get a Single User:

# GET /users/:userId
# Create a User:

# POST /users
# Update a User:

# PUT /users/:userId or PATCH /users/:userId
# Delete a User:

# DELETE /users/:userId
# Searches
# List Searches:

# GET /searches
# Get a Single Search:

# GET /searches/:searchId
# Create a Search:

# POST /searches
# Update a Search:

# PUT /searches/:searchId or PATCH /searches/:searchId
# Delete a Search:

# DELETE /searches/:searchId
# Jobs
# List Jobs:

# GET /jobs
# Get a Single Job:

# GET /jobs/:jobId
# Create a Job:

# POST /jobs
# Update a Job:

# PUT /jobs/:jobId or PATCH /jobs/:jobId
# Delete a Job:

# DELETE /jobs/:jobId
