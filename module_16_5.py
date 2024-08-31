from fastapi import FastAPI, Body, HTTPException, status, Request, Form, Path
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

templates= Jinja2Templates(directory='templates')

app = FastAPI()

class User(BaseModel):
    id: int = None
    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='User')] = 'User'
    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=22)] = 22

users: List[User] = [
    User(id=1, username='UrbanUser', age=24),
    User(id=2, username='UrbanTest', age=22),
    User(id=3, username='Capybara', age=60)
]

@app.get('/')
async def get_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/users/{user_id}')
async def get_user_page(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')

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
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)],
     username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='UrbanUser')],
     age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=25)]):
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