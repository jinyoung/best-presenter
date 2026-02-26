from __future__ import annotations

import asyncio
import json

from langchain_openai import ChatOpenAI

from app.config import settings
from app.graph.pipeline import pipeline
from app.models.schemas import (
    EvaluateRequest,
    EvaluateResponse,
    MultiSpeakerResponse,
    SpeakerContribution,
)
from app.prompts.contribution import CONTRIBUTION_SYSTEM, CONTRIBUTION_USER
from app.utils.text import SpeakerSegment, group_by_speaker, parse_vtt


async def run_evaluation(request: EvaluateRequest) -> EvaluateResponse:
    initial_state = {
        "transcript": request.transcript,
        "audience": request.audience or "",
        "purpose": request.purpose or "",
        "remove_fillers": request.remove_fillers,
    }

    result = await pipeline.ainvoke(initial_state)
    return result["response"]


async def _evaluate_speaker(speaker: str, text: str, request: EvaluateRequest) -> tuple[str, EvaluateResponse]:
    """Run the standard pipeline for a single speaker's text."""
    speaker_request = EvaluateRequest(
        transcript=text,
        audience=request.audience,
        purpose=request.purpose,
        remove_fillers=request.remove_fillers,
    )
    result = await run_evaluation(speaker_request)
    return speaker, result


async def _generate_contributions(
    segments: list[SpeakerSegment],
    speaker_texts: dict[str, str],
    full_transcript: str,
) -> list[SpeakerContribution]:
    """Generate contribution summaries for each speaker via LLM."""
    # Compute basic stats
    speaker_stats_parts: list[str] = []
    total_words = sum(len(t.split()) for t in speaker_texts.values())
    contributions: dict[str, SpeakerContribution] = {}

    for speaker, text in speaker_texts.items():
        utterance_count = sum(1 for s in segments if s.speaker == speaker)
        word_count = len(text.split())
        ratio = word_count / total_words if total_words > 0 else 0
        contributions[speaker] = SpeakerContribution(
            speaker=speaker,
            utterance_count=utterance_count,
            word_count=word_count,
            speaking_ratio=round(ratio, 3),
        )
        speaker_stats_parts.append(
            f"- {speaker}: 발화 {utterance_count}회, {word_count}단어, 비율 {ratio:.1%}"
        )

    # LLM call for role summaries
    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )
    prompt_user = CONTRIBUTION_USER.format(
        speakers=", ".join(speaker_texts.keys()),
        speaker_stats="\n".join(speaker_stats_parts),
        full_transcript=full_transcript[:6000],
    )
    response = await llm.ainvoke([
        {"role": "system", "content": CONTRIBUTION_SYSTEM},
        {"role": "user", "content": prompt_user},
    ])

    # Parse LLM response
    try:
        content = response.content
        # Extract JSON array from response
        start = content.index("[")
        end = content.rindex("]") + 1
        role_data = json.loads(content[start:end])
        for item in role_data:
            speaker = item.get("speaker", "")
            if speaker in contributions:
                contributions[speaker].role_summary = item.get("role_summary", "")
    except (ValueError, json.JSONDecodeError):
        pass  # Keep empty role_summary if parsing fails

    return list(contributions.values())


async def run_multi_speaker_evaluation(
    request: EvaluateRequest,
) -> MultiSpeakerResponse:
    """Orchestrate per-speaker evaluations and contribution summary."""
    segments = parse_vtt(request.transcript)
    speaker_texts = group_by_speaker(segments)
    speakers = list(speaker_texts.keys())

    # Run per-speaker evaluations concurrently
    tasks = [
        _evaluate_speaker(speaker, text, request)
        for speaker, text in speaker_texts.items()
    ]
    results = await asyncio.gather(*tasks)
    evaluations = {speaker: result for speaker, result in results}

    # Generate contribution summary (single LLM call)
    # Reconstruct full transcript from segments for context
    full_transcript = "\n".join(
        f"{seg.speaker}: {seg.text}" for seg in segments
    )
    contributions = await _generate_contributions(
        segments, speaker_texts, full_transcript
    )

    return MultiSpeakerResponse(
        speakers=speakers,
        contributions=contributions,
        evaluations=evaluations,
    )
