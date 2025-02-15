from typing import List, Dict

from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import service
from app.database import async_session_maker, engine
from app.models import models

import sys


print(sys.path)
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

# CRUD методы
@app.get("/test")
async def get_questions(db: AsyncSession = Depends(get_db)):
    questions = await service.get_questions(db=db)
    return questions

@app.put("/test/{test_id}")
async def generate_recommendations(test_id: int, incorrect_themes: List[str] = Query(..., description="List of incorrect themes"), db: AsyncSession = Depends(get_db)):
    recommendations = await service.generate_recommendations(db=db, test_id=test_id, incorrect_themes=incorrect_themes)
    if recommendations is None:
        return {
            "message": "Test not found"
        }
    return recommendations

@app.post("/test")
async def save_test(result: int, db: AsyncSession = Depends(get_db)):
    test = await service.create_test(db=db, result=result)
    return {
        "test_id": test.id,
        "trainee": test.trainee,
        "result": test.result
    }

@app.get("/recommendations")
async def get_recommendations(db: AsyncSession = Depends(get_db)):
    return await service.get_materials(db=db)

@app.put("/recommendations")
async def save_chosen_recommendations(chosen_materials: Dict[str, List[str]], db: AsyncSession = Depends(get_db)):
    return await service.edit_materials(db=db, chosen_materials=chosen_materials)

@app.post("/iprs")
async def create_ipr(db: AsyncSession = Depends(get_db)):
    return await service.create_ipr(db=db)

@app.put("/iprs")
async def edit_ipr(progress: int, db: AsyncSession = Depends(get_db)):
    return await service.edit_ipr(db=db, progress=progress)


@app.get("/interviews")
async def get_interviews(db: AsyncSession = Depends(get_db)):
    return await service.get_interviews(db=db)
