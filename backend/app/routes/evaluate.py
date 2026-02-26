from fastapi import APIRouter, HTTPException

from app.models.db import save_evaluation, save_multi_speaker_evaluation
from app.models.schemas import EvaluateRequest, EvaluateResponse, MultiSpeakerResponse
from app.services.evaluation import run_evaluation, run_multi_speaker_evaluation
from app.utils.text import is_vtt

router = APIRouter()


@router.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    try:
        use_vtt = request.format == "vtt" or (request.format is None and is_vtt(request.transcript))

        if use_vtt:
            response = await run_multi_speaker_evaluation(request)
            result_dict = response.model_dump(by_alias=True)
            eval_id = await save_multi_speaker_evaluation(request.transcript, result_dict)
            response.id = eval_id
            return response
        else:
            response = await run_evaluation(request)
            result_dict = response.model_dump(by_alias=True)
            eval_id = await save_evaluation(request.transcript, result_dict)
            response.id = eval_id
            return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
