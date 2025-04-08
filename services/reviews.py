from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.reviews import Review
from app.schemas.reviews import CreateReview, ReadReview, UpdateReview
from app.services import BaseService

class ReviewServices(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['reviews']

    async def create_review(self, book_id: str, review_data: CreateReview):
        review = Review(**review_data.dict())
        review_data_get = review.dict()
        review_data_get['book_id'] = book_id
        result = await self.collection.insert_one(review_data_get)
        # await self.collection.insert_one({'book_id' : book_id})
        # result = await self.collection.insert_one(review.dict())
        review = await self.collection.find_one({'_id': result.inserted_id})
        return self._to_response(review, ReadReview)
         
    async def get_review(self, book_id: str):
        try:
            book_review = await self.collection.find({'book_id': book_id}).to_list(length=None)
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid BookID")
        if not book_review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book ID Not Found')
        
        return [self._to_response(review, ReadReview) for review in book_review]

    async def update_review(self, review_id: str, update_data: UpdateReview):
        try:
            result = await self.collection.update_one({'_id': ObjectId(review_id)},
                                                      {'$set' : update_data.dict(exclude_unset=True)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectID")
        if not result.matched_count:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Review Not Found')
        review = await self.collection.find_one({'_id' : ObjectId(review_id)})
        return self._to_response(review, ReadReview)
    
    async def delete_review(self, review_id: str):
        try:
            result = await self.collection.delete_one({'_id' : ObjectId(review_id)})
            if not result.deleted_count:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="review Not Found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId")
