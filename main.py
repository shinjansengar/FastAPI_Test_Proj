from typing import List
from uuid import UUID
from fastapi import FastAPI,HTTPException
from models import Gender, Role, User, UserUpdateModel

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("829c950b-66a8-4411-b41f-69a55442c1a0"),
        first_name='Shinjan',
        last_name='Sengar',
        gender=Gender.male,
        roles=[Role.admin,Role.user]
        ),
    User(
        id=UUID("bcf8cdd0-462e-49fb-920b-d40dd0edd953"),
        first_name='Divya',
        last_name='Gupta',
        gender=Gender.female,
        roles=[Role.user]
        ),
]

@app.get("/")
async def root():
    return {"Hello":"Shinjan"}

@app.get("/api/v1/users")
async def users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id":user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return 
    raise HTTPException(
        status_code=404,
        detail=f"User with user id {user_id} does not exists."
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateModel,user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name != None:
                user.first_name = user_update.first_name
            if user_update.last_name != None:
                user.last_name = user_update.last_name
            if user_update.middle_name != None:
                user.middle_name = user_update.middle_name
            if user_update.roles != None:
                user.roles = user_update.roles
            return

    raise HTTPException(
        status_code=404,
        detail=f"User with user id {user_id} does not exists."
    )