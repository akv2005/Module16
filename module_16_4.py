from fastapi import FastAPI, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int = None
    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='User')] = 'User'
    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=22)] = 22

users: List[User] = []

@app.get('/users')
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_user(user: User,
    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='UrbanUser')],
    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=25)]):
    len_user = len(users)
    if len_user == 0:
        user.id = 1
    else:
        user.id = users[len_user - 1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    return f'User {user} is registered'

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)],
     username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='UrbanUser')],
     age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=25)]):
#async def update_user(user_id: int, username: str, age: int):
    raise1 = True
    for edit_user in users:
        if edit_user.id == user_id:
            edit_user.username = username
            edit_user.age = age
            return edit_user
    if raise1:
        raise HTTPException(status_code=404, detail='User was not found')
@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    raise2 = True
    ind_del = 0
    for delete_user in users:
        if delete_user.id == user_id:
            users.pop(ind_del)
            return delete_user
        ind_del += 1
    if raise2:
        raise HTTPException(status_code=404, detail='User was not found')
