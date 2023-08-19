import secrets

from bson import ObjectId
from typing import Annotated
from fastapi import Depends, APIRouter
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.users import CreateUser
from utils.database import get_db
from fastapi.responses import JSONResponse
import hashlib
from utils.exceptions import DuplicateRecord, Unauthorized
from utils.exceptions import NotFoundRecord

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


#Encriptar contraseña


@router.post("")
async def create_user(
    create_user: CreateUser,
    database: AsyncIOMotorDatabase = Depends(get_db),
):
    user_exists = await database.users.find_one({
        "email": create_user.email
    })

    if user_exists:
        raise DuplicateRecord(f"User {create_user.email} already exists")
    
    def hash_password(password):
        salt = b'some_random_salt'  # Cambia esto por un valor aleatorio en un entorno de producción
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return hashed_password

    hashed_password = hash_password(create_user.password)  # Encriptar la contraseña

    inserted_id = await database.users.insert_one(
        {
            "_id": str(ObjectId()),
            "email": create_user.email,
            "password": hashed_password,  # Almacenar la contraseña encriptada
            "firstname": create_user.firstname,
            "lastname": create_user.lastname,
            "token": secrets.token_hex(12),
        }
    )

    return JSONResponse(
        content={"created_user": str(inserted_id.inserted_id)},
        status_code=201
    )


@router.get("/{user_id}")
async def get_user(
    database : Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    user_id : str,
):
    user = await database.users.find_one(
        {
            "_id": user_id,
        }
    )

    if not user:
        raise NotFoundRecord(f"User with id {user_id} does not exists")


    # Convertir el resultado a un diccionario antes de enviarlo como JSON
    user_dict = {
        "_id": user["_id"],
        "email": user["email"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "token":user["token"],
    }

    return JSONResponse(
        content=user_dict,
        status_code=200,
    )

@router.get("/{email}/{password}")
async def login(
    database : Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    email : str,
    password : str,
):
    def hash_password(password):
        salt = b'some_random_salt'  # Cambia esto por un valor aleatorio en un entorno de producción
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return hashed_password

    user = await database.users.find_one(
        {
            "email": email,
        }
    )

    if not user:
        raise NotFoundRecord(f"User with emial {email} does not exists")


    # Encriptar la contraseña proporcionada por el usuario y compararla con la almacenada
    hashed_password_input = hash_password(password)
    if user["password"] != hashed_password_input:
        raise Unauthorized(f"Incorrect password")


    user_dict = {
        "_id": user["_id"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "token": user["token"],
    }

    return JSONResponse(
        content=user_dict,
        status_code=200,
    )
