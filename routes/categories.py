from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.categories import CreateCategory, ReadCategory, UpdateCategory
from app.services.categories import CategoryService
from app.database import get_database

category_router = APIRouter(tags=['Category'])
logger = logging.getLogger(__name__)

def category_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return CategoryService(db)

@category_router.post("/create_category", response_model=ReadCategory)
async def create_category(request: Request, category: CreateCategory, service: CategoryService = Depends(category_service)):
    logger.info(f'Request path: {request.url.path}')
    try:
        return await service.create_category(category)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@category_router.get("/get_category", response_model=ReadCategory)
async def get_category(request: Request, category_id: str, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_category(category_id=category_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f'Exception : {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@category_router.put("/update_category", response_model=ReadCategory)
async def update_category(request: Request, category_id: str, category: UpdateCategory, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        updated_category = await service.update_category(category_id=category_id, update_data=category)
        return updated_category
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f'Exception: {str(e)}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@category_router.delete("/delete_category")
async def delete_category(request: Request, category_id: str, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_category(category_id=category_id)
        return f"The CategoryId: {category_id} is deleted"
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@category_router.get('/get_categories', response_model=List[ReadCategory])
async def get_categories(request: Request, service: CategoryService = Depends(category_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_categories()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")