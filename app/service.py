# ������� ��������� ����� �� ������� API
import json
from typing import List, Dict

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import *


async def get_questions(db: AsyncSession):
    # select_query = select(Question.question, Question.theme, Question.answer).order_by(func.random()).limit(10)
    result = await db.execute(
        select(Question.theme, Question.question, Question.answer).order_by(func.random()).limit(10))
    return result.mappings().all()


async def generate_recommendations(db: AsyncSession, test_id: int, incorrect_themes: List[str]):
    test = await db.execute(select(Test).where(Test.id == test_id))
    test = test.scalars().first()

    if not test:
        return None

    recommendations = {}

    for theme in incorrect_themes:
        result = await db.execute(select(Recommendation).filter(Recommendation.theme == theme).limit(2))

        theme_recommendations = result.scalars().all()

        if theme_recommendations:
            recommendations[theme] = [rec.material for rec in theme_recommendations]

    test.recommendations = json.dumps(recommendations, ensure_ascii=False)
    await db.commit()
    await db.refresh(test)
    return recommendations


async def create_test(db: AsyncSession, result: int):
    db_test = Test(trainee="Shafikov Artur", result=result, recommendations="None")
    db.add(db_test)
    await db.commit()
    await db.refresh(db_test)
    return db_test


async def get_materials(db: AsyncSession):
    tests_with_recommendations = await db.execute(select(Test).where(Test.recommendations != None))
    tests_with_recommendations = tests_with_recommendations.scalars().all()

    test_recommendations = []
    for test in tests_with_recommendations:
        try:
            # Load the JSON string into a Python dictionary
            recommendations_dict = json.loads(test.recommendations)
            test_recommendations.append(recommendations_dict)
        except (json.JSONDecodeError, TypeError):
            # Handle the case where the value is not a valid JSON string or is None
            print(f"Skipping invalid recommendations for test ID: {test.id}")
            continue

    # Fetch all recommendations from Recommendations
    all_recommendations = await db.execute(select(Recommendation))
    all_recommendations = all_recommendations.scalars().all()

    recommendations_list = [{"theme": rec.theme, "material": rec.material} for rec in all_recommendations]

    # if (tests_with_recommendations != None):
    chosen_materials = await db.execute(select(Chosen_materials).where(Chosen_materials.id == 1))
    chosen_materials_instance = chosen_materials.scalars().first()
    chosen_materials_instance.materials = json.dumps(test_recommendations, ensure_ascii=False)
    db.add(chosen_materials_instance)
    await db.commit()
    await db.refresh(chosen_materials_instance)

    return {
        "mandatory_recommendations": test_recommendations,
        "optional_recommendations": recommendations_list
    }


async def edit_materials(chosen_materials: Dict[str, List[str]], db: AsyncSession):
    chosen_materials_table = await db.execute(select(Chosen_materials).where(Chosen_materials.id == 1))
    chosen_materials_instance = chosen_materials_table.scalars().first()
    chosen_materials_instance.materials = json.dumps(chosen_materials, ensure_ascii=False)
    db.add(chosen_materials_instance)
    await db.commit()
    await db.refresh(chosen_materials_instance)
    return


async def create_ipr(db: AsyncSession):
    ch_mat_t = await db.execute(select(Chosen_materials).where(Chosen_materials.id == 1))
    ch_mat_instance = ch_mat_t.scalars().first()

    ipr_t = await db.execute(select(IPR).where(IPR.id == 1))
    ipr_instance = ipr_t.scalars().first()

    if not ipr_instance:
        ipr = IPR(id=1, progress=0, is_approved=True)
        db.add(ipr)
        await db.commit()
        await db.refresh(ipr)

    return json.loads(ch_mat_instance.materials)


async def edit_ipr(db: AsyncSession, progress: int):
    ipr_t = await db.execute(select(IPR).where(IPR.id == 1))
    ipr_instance = ipr_t.scalars().first()

    ipr_instance.progress = progress
    await db.commit()
    await db.refresh(ipr_instance)
    return ipr_instance


async def get_interviews(db: AsyncSession):
    all_interviews = await db.execute(select(Interview))
    return all_interviews.scalars().all()
