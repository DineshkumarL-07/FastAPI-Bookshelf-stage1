from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.users import UserService
from app.database import get_database

user_router = APIRouter(tags=['Users'])
logger = logging.getLogger(__name__)

def user_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return UserService(db)

@user_router.get("/get_users", response_model=List[UserRead])
async def get_users(request: Request, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_users()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
    
@user_router.post("/users", response_model=UserRead)
async def create_user(request: Request, user: UserCreate, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_user(user)
    except HTTPException as e:
        logger.error(f'HTTPException: {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'Exception: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    
@user_router.get("/users/{user_id}", response_model=UserRead)
async def get_user(request: Request, user_id: str, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        user = await service.get_user(user_id=user_id)
        return user
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@user_router.put("/users/{user_id}", response_model=UserRead)
async def update_user(request: Request, user_id: str, user: UserUpdate,  service: UserService = Depends(user_service)):
    logger.info(f'Request path: {request.url.path}')
    try:
        update_user = await service.update_user(user_id=user_id, update_data=user)
        return update_user
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    
@user_router.delete("/users/{user_id}")
async def delete_user(request: Request, user_id: str, service: UserService = Depends(user_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_user(user_id=user_id)
        return f"User who is having the {user_id}, is deleted"
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')