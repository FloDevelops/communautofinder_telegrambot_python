import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
# from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from back_reservauto.database import SessionLocal, engine
from back_reservauto import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/users')
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

@app.get('/users/{user_id}')
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return db_user

@app.post('/users')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(user.telegram_user_id, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    return crud.create_user(user, db)

@app.put('/users/{user_id}')
def update_user(user_id: str, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return crud.update_user(user, db)

@app.delete('/users/{user_id}')
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return crud.delete_user(user_id, db)


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
