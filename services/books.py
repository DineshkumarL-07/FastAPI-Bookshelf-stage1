from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase

from fastapi import HTTPException, status
from app.models.books import Book
from app.schemas.books import BookCreate, BookResponse, BookUpdate
from app.services import BaseService


class BookService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['books']

    async def create_book(self, book_data: BookCreate):
        book = Book(**book_data.dict())
        result = await self.collection.insert_one(book.dict())
        book = await self.collection.find_one({'_id': result.inserted_id})
        return self._to_response(book, BookResponse)

    async def get_book(self, book_id: str):
        try:
            book = await self.collection.find_one({'_id': ObjectId(book_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return self._to_response(book, BookResponse)

    async def update_book(self, book_id: str, update_data: BookUpdate):
        try:
            result = await self.collection.update_one({'_id': ObjectId(book_id)},
                                                      {'$set': update_data.dict(exclude_unset=True)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        book = await self.collection.find_one({'_id': ObjectId(book_id)})
        return self._to_response(book, BookResponse)

    async def delete_book(self, book_id: str):
        try:
            result = await self.collection.delete_one({'_id': ObjectId(book_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")

    async def get_books(self):
        books = await self.collection.find().to_list(None)
        return [self._to_response(book, BookResponse) for book in books]
