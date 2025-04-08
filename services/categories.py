from bson.objectid import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from app.models.categories import Category
from app.schemas.categories import CreateCategory, ReadCategory, UpdateCategory
from app.services import BaseService

class CategoryService(BaseService):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db)
        self.collection = db['category']
    
    async def create_category(self, category_data: CreateCategory):
        category = Category(**category_data.dict())
        result = await self.collection.insert_one(category.dict())
        category = await self.collection.find_one({'_id' : result.inserted_id})
        return self._to_response(category, ReadCategory)

    async def get_category(self, category_id: str):
        try:
            category = await self.collection.find_one({'_id' : ObjectId(category_id)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectID")
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Id not found")
        return self._to_response(category, ReadCategory)

    async def update_category(self, category_id: str, update_data: UpdateCategory):
        try:
            result = await self.collection.update_one({'_id' : ObjectId(category_id)},
                                                      {'$set' : update_data.dict(exclude_unset=True)})
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectID")
        if not result.matched_count:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
        category = await self.collection.find_one({'_id' : ObjectId(category_id)})
        return self._to_response(category, ReadCategory)
    
    async def delete_category(self, category_id: str):
        try:
            result = await self.collection.delete_one({'_id' : ObjectId(category_id)})
            if not result.deleted_count:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectID")
        
    async def get_categories(self):
        categories = await self.collection.find().to_list(None)
        return [self._to_response(category, ReadCategory) for category in categories]
    