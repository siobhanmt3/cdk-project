from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorDatabase

from fastapi import APIRouter, Depends

from models.products import CreateProduct, UpdateProduct
from utils.database import get_db
from fastapi.responses import JSONResponse
from bson import ObjectId

from utils.validate_token import validate_token
from utils.exceptions import NotFoundRecord


router = APIRouter(
    prefix="/Products",
    tags=["Products"],
)


@router.post("", dependencies=[Depends(validate_token)])
async def create_product(
    create_product: CreateProduct,
    database: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
):
    inserted_id = await database.products.insert_one(
        {
            "_id": str(ObjectId()),
            "user_token": create_product.user_token,
            "name": create_product.name,
            "description": create_product.description,
            "category": create_product.category,
        }
    )
    return JSONResponse(
        content={"Created_product": inserted_id.inserted_id}, status_code=201
    )


# ---  GET LIST OF PRODUCTS CREATED BY A USER
@router.get("/{user_token}")
async def get_product(
    database: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    user_token: str,
):
    products = await database.products.find(
        {
            "user_token": user_token,
        }
    ).to_list(length=None)

    if not user_token:
        raise NotFoundRecord(f"User with id {user_token} does not exists")

    if not products:
        raise NotFoundRecord("Products not found")

    return JSONResponse(content=products, status_code=200)


# --- UPDATE PRODUCT
@router.put("/{product_id}", dependencies=[Depends(validate_token)])
async def update_product(
    product_id: str,
    update_data: UpdateProduct,
    database: AsyncIOMotorDatabase = Depends(get_db),
):
    existing_product = await database.products.find_one({"_id": product_id})
    if not existing_product:
        raise NotFoundRecord(f"Product with id {product_id} does not exists")

    updated_product = {
        "name": update_data.name,
        "description": update_data.description,
        "category": update_data.category,
    }

    await database.products.update_one({"_id": product_id}, {"$set": updated_product})

    return JSONResponse(
        content={"message": f"Product {product_id} updated successfully"},
        status_code=200,
    )


# --- DELETE PRODUCT
@router.delete("/{product_id}", dependencies=[Depends(validate_token)])
async def delete_product(
    product_id: str,
    database: AsyncIOMotorDatabase = Depends(get_db),
):
    existing_product = await database.products.find_one({"_id": product_id})
    if not existing_product:
        raise NotFoundRecord(f"Product with id {product_id} does not exists")

    await database.products.delete_one({"_id": product_id})

    return JSONResponse(
        content={"message": f"Product {product_id} deleted successfully"},
        status_code=200,
    )
