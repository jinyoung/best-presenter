from __future__ import annotations

from typing import TypedDict

from app.models.schemas import (
    ClassificationResult,
    CoachingResult,
    DerivedMetrics,
    EvaluateResponse,
    EvidenceResult,
    ScoringResult,
    VerificationResult,
)


class PipelineState(TypedDict, total=False):
    # Input
    transcript: str
    audience: str
    purpose: str
    remove_fillers: bool

    # preprocess
    cleaned_text: str
    sentences: list[str]

    # classify
    classification: ClassificationResult

    # evidence
    evidence: EvidenceResult

    # score
    scoring: ScoringResult
    verification: VerificationResult
    derived_metrics: DerivedMetrics
    final_axis_scores: dict[str, int]  # axis -> 0-100

    # coach
    coaching: CoachingResult

    # compose
    response: EvaluateResponse
