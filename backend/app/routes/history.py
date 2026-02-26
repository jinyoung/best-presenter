from fastapi import APIRouter, HTTPException

from app.models.db import get_evaluation, list_evaluations

router = APIRouter()


@router.get("/evaluations")
async def get_evaluations(limit: int = 20):
    return await list_evaluations(limit)


@router.get("/evaluations/{eval_id}")
async def get_evaluation_detail(eval_id: str):
    result = await get_evaluation(eval_id)
    if not result:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return result
