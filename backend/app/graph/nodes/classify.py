from langchain_openai import ChatOpenAI

from app.config import settings
from app.models.schemas import ClassificationResult
from app.models.state import PipelineState
from app.prompts.classify import CLASSIFY_SYSTEM, CLASSIFY_USER


def classify(state: PipelineState) -> dict:
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    ).with_structured_output(ClassificationResult)

    audience_hint = f"사용자 지정 청중: {state['audience']}" if state.get("audience") else "청중 정보 없음 (자동 추정)"
    purpose_hint = f"사용자 지정 목적: {state['purpose']}" if state.get("purpose") else "목적 정보 없음 (자동 추정)"

    user_msg = CLASSIFY_USER.format(
        transcript=state["cleaned_text"][:3000],
        audience_hint=audience_hint,
        purpose_hint=purpose_hint,
    )

    result = llm.invoke([
        {"role": "system", "content": CLASSIFY_SYSTEM},
        {"role": "user", "content": user_msg},
    ])

    return {"classification": result}
