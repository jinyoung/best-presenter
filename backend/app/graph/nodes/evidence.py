from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.config import settings
from app.models.schemas import EvidenceResult
from app.models.state import PipelineState
from app.prompts.evidence import AXES_CHECKPOINTS, EVIDENCE_SYSTEM, EVIDENCE_USER


def _format_checkpoints() -> str:
    lines = []
    for axis, cps in AXES_CHECKPOINTS.items():
        lines.append(f"\n[{axis}]")
        for i, cp in enumerate(cps, 1):
            lines.append(f"  {i}. {cp}")
    return "\n".join(lines)


def _number_sentences(sentences: list[str]) -> str:
    return "\n".join(f"s{i+1}: {s}" for i, s in enumerate(sentences))


def evidence(state: PipelineState) -> dict:
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    ).with_structured_output(EvidenceResult)

    classification = state["classification"]
    user_msg = EVIDENCE_USER.format(
        intent=classification.intent,
        audience=classification.audience_level,
        domain=classification.domain,
        checkpoints_text=_format_checkpoints(),
        numbered_transcript=_number_sentences(state["sentences"]),
    )

    result = llm.invoke([
        {"role": "system", "content": EVIDENCE_SYSTEM},
        {"role": "user", "content": user_msg},
    ])

    return {"evidence": result}
