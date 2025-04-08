from fastapi import APIRouter, Depends, HTTPException, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
import logging
from app.schemas.books import BookCreate, BookUpdate, BookResponse
from app.services.books import BookService
from app.database import get_database

router = APIRouter(prefix='/books', tags=['Books'])
logger = logging.getLogger(__name__)


def book_service(db: AsyncIOMotorDatabase = Depends(get_database)):
    return BookService(db)


@router.get("", response_model=List[BookResponse])
async def get_books(request: Request, service: BookService = Depends(book_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.get_books()
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(request: Request, book: BookCreate, service: BookService = Depends(book_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        return await service.create_book(book)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(request: Request, book_id: str, service: BookService = Depends(book_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        book = await service.get_book(book_id)
        return book
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(request: Request, book_id: str, book: BookUpdate, service: BookService = Depends(book_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        updated_book = await service.update_book(book_id, book)
        return updated_book
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(request: Request, book_id: str, service: BookService = Depends(book_service)):
    logger.info(f"Request path: {request.url.path}")
    try:
        await service.delete_book(book_id)
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
