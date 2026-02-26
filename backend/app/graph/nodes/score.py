from __future__ import annotations

import json

from langchain_openai import ChatOpenAI

from app.config import settings
from app.models.schemas import (
    DerivedMetrics,
    ScoringResult,
    VerificationResult,
)
from app.models.state import PipelineState
from app.prompts.evidence import AXES_CHECKPOINTS
from app.prompts.score import SCORE_SYSTEM, SCORE_USER, VERIFY_SYSTEM, VERIFY_USER
from app.services.rule_metrics import compute_all_metrics


RULE_AXIS_MAP = {
    "evidence_specificity": "numeric_sentence_ratio",
    "logical_coherence": "logic_marker_ratio",
}

RULE_ADJUSTMENTS = {
    "numeric_sentence_ratio": {"threshold_low": 0.1, "threshold_high": 0.3, "adjustment": 3},
    "logic_marker_ratio": {"threshold_low": 0.1, "threshold_high": 0.25, "adjustment": 3},
}


def _evidence_to_text(state: PipelineState) -> str:
    lines = []
    for axis_ev in state["evidence"].axes:
        lines.append(f"\n[{axis_ev.axis}]")
        for cp_ev in axis_ev.checkpoints:
            lines.append(f"  체크포인트: {cp_ev.checkpoint}")
            if cp_ev.positive:
                lines.append("    가점 증거:")
                for q in cp_ev.positive:
                    lines.append(f"      - [{q.loc}] {q.text}")
            if cp_ev.negative:
                lines.append("    감점 증거:")
                for q in cp_ev.negative:
                    lines.append(f"      - [{q.loc}] {q.text}")
    return "\n".join(lines)


def _scoring_to_text(scoring: ScoringResult) -> str:
    lines = []
    for axis_s in scoring.axes:
        lines.append(f"\n[{axis_s.axis}]")
        for cp_s in axis_s.checkpoints:
            lines.append(f"  {cp_s.checkpoint}: {cp_s.earned}/{cp_s.max_score} - {cp_s.reasoning}")
    return "\n".join(lines)


def _compute_axis_scores(scoring: ScoringResult, verification: VerificationResult, metrics: dict) -> dict[str, int]:
    verified = {}
    for v in verification.verifications:
        verified[(v.axis, v.checkpoint)] = v.verified_score

    axis_scores = {}
    for axis_s in scoring.axes:
        total_earned = 0
        total_max = 0
        for cp_s in axis_s.checkpoints:
            key = (axis_s.axis, cp_s.checkpoint)
            earned = verified.get(key, cp_s.earned)
            total_earned += earned
            total_max += cp_s.max_score

        if total_max > 0:
            raw_score = round(total_earned / total_max * 100)
        else:
            raw_score = 0

        # Rule-based adjustment
        metric_key = RULE_AXIS_MAP.get(axis_s.axis)
        if metric_key and metric_key in metrics:
            adj_config = RULE_ADJUSTMENTS[metric_key]
            val = metrics[metric_key]
            if val < adj_config["threshold_low"]:
                raw_score = max(0, raw_score - adj_config["adjustment"])
            elif val > adj_config["threshold_high"]:
                raw_score = min(100, raw_score + adj_config["adjustment"])

        # Vagueness penalty applies to audience_fit
        if axis_s.axis == "audience_fit" and metrics.get("vagueness_index", 0) > 0.2:
            raw_score = max(0, raw_score - 3)

        axis_scores[axis_s.axis] = max(0, min(100, raw_score))

    return axis_scores


def score(state: PipelineState) -> dict:
    llm_score = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    ).with_structured_output(ScoringResult)

    llm_verify = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    ).with_structured_output(VerificationResult)

    evidence_text = _evidence_to_text(state)

    # Pass 1: Initial scoring
    scoring = llm_score.invoke([
        {"role": "system", "content": SCORE_SYSTEM},
        {"role": "user", "content": SCORE_USER.format(evidence_text=evidence_text)},
    ])

    # Pass 2: Self-verification
    scoring_text = _scoring_to_text(scoring)
    verification = llm_verify.invoke([
        {"role": "system", "content": VERIFY_SYSTEM},
        {"role": "user", "content": VERIFY_USER.format(
            scoring_text=scoring_text,
            evidence_text=evidence_text,
        )},
    ])

    # Rule-based metrics
    metrics = compute_all_metrics(state["sentences"])
    derived = DerivedMetrics(**metrics)

    axis_scores = _compute_axis_scores(scoring, verification, metrics)

    return {
        "scoring": scoring,
        "verification": verification,
        "derived_metrics": derived,
        "final_axis_scores": axis_scores,
    }
