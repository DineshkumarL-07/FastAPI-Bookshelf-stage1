from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.reviews import CreateReview, ReadReview, UpdateReview
from app.services.reviews import ReviewServices
from app.database import get_database

review_router = APIRouter(tags=["Review"])
logger = logging.getLogger(__name__)

def review_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return ReviewServices(db)

@review_router.post("/books/{book_id}/reviews", response_model=ReadReview)
async def create_review(request: Request, review: CreateReview, book_id: str, service: ReviewServices = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_review(book_id=book_id, review_data=review)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')

@review_router.get("/books/{book_id}/reviews", response_model=List[ReadReview])
async def get_review(request: Request, book_id: str, service: ReviewServices = Depends(review_service)):
    logger.info(f"request path: {request.url.path}")
    try:
        return await service.get_review(book_id = book_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@review_router.put("/books/{book_id}/reviews/{review_id}", response_model=ReadReview)
async def update_review(request: Request,book_id: str, review_id: str,review: UpdateReview, service: ReviewServices = Depends(review_service)):
    logger.info(f"Request Path: {request.url.path}")
    try:
        updated_review = await service.update_review(review_id = review_id, update_data=review)
        return updated_review
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
@review_router.delete("/books/{book_id}/reviews/{review_id}")
async def delete_review(request: Request, book_id: str,  review_id: str, service: ReviewServices = Depends(review_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_review(review_id)
        return f"The reviewId named {review_id}, is deleted"
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
