from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users

from app.users.shemas import SUsersAuth

router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация и Пользователи'],
)


@router.post('/register')
async def register_user(user_data: SUsersAuth):
    exicting_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if exicting_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_date: SUsersAuth):
    user = await authenticate_user(user_date.email, user_date.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.post('/me')
async def reade_user_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.post('/all')
async def reade_user_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()