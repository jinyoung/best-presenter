from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.config import settings
from app.models.schemas import CoachingResult
from app.models.state import PipelineState
from app.prompts.coach import COACH_SYSTEM, COACH_USER

AXIS_LABELS = {
    "purpose_clarity": "목적 명확성",
    "structure": "구조",
    "evidence_specificity": "근거 구체성",
    "audience_fit": "청중 적합성",
    "logical_coherence": "논리 일관성",
    "decision_support": "의사결정 지원",
}


def _format_axis_scores(axis_scores: dict[str, int]) -> str:
    lines = []
    for axis, score in sorted(axis_scores.items(), key=lambda x: x[1]):
        label = AXIS_LABELS.get(axis, axis)
        lines.append(f"  {label} ({axis}): {score}/100")
    return "\n".join(lines)


def _find_weak_checkpoints(state: PipelineState) -> str:
    lines = []
    verified = {}
    for v in state["verification"].verifications:
        verified[(v.axis, v.checkpoint)] = v.verified_score

    for axis_s in state["scoring"].axes:
        for cp_s in axis_s.checkpoints:
            earned = verified.get((axis_s.axis, cp_s.checkpoint), cp_s.earned)
            if earned <= 2:
                lines.append(f"  [{axis_s.axis}] {cp_s.checkpoint}: {earned}/5 - {cp_s.reasoning}")

    return "\n".join(lines) if lines else "  감점 체크포인트 없음"


def coach(state: PipelineState) -> dict:
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.7,
    ).with_structured_output(CoachingResult)

    classification = state["classification"]
    user_msg = COACH_USER.format(
        intent=classification.intent,
        audience=classification.audience_level,
        axis_scores_text=_format_axis_scores(state["final_axis_scores"]),
        weak_checkpoints_text=_find_weak_checkpoints(state),
        transcript=state["cleaned_text"][:4000],
    )

    result = llm.invoke([
        {"role": "system", "content": COACH_SYSTEM},
        {"role": "user", "content": user_msg},
    ])

    return {"coaching": result}
