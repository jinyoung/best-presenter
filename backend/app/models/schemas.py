from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# --- LLM Structured Output Models ---


class ClassificationResult(BaseModel):
    intent: str = Field(description="발표 의도: project_status | architecture | decision_request | persuasion | education")
    audience_level: str = Field(description="청중 수준: executive | pm | engineer | customer | auditor")
    domain: str = Field(description="도메인: tech | project | business | general")
    confidence: float = Field(ge=0, le=1, description="분류 신뢰도")


class EvidenceQuote(BaseModel):
    text: str = Field(description="증거 문장 원문")
    loc: str = Field(description="위치 (예: s3)")
    sentiment: str = Field(description="positive | negative")


class CheckpointEvidence(BaseModel):
    checkpoint: str = Field(description="체크포인트 이름")
    positive: list[EvidenceQuote] = Field(default_factory=list)
    negative: list[EvidenceQuote] = Field(default_factory=list)


class AxisEvidence(BaseModel):
    axis: str
    checkpoints: list[CheckpointEvidence]


class EvidenceResult(BaseModel):
    axes: list[AxisEvidence]


class CheckpointScore(BaseModel):
    checkpoint: str
    max_score: int = 5
    earned: int = Field(ge=0, le=5)
    reasoning: str


class AxisScore(BaseModel):
    axis: str
    checkpoints: list[CheckpointScore]


class ScoringResult(BaseModel):
    axes: list[AxisScore]


class ScoringVerification(BaseModel):
    axis: str
    checkpoint: str
    original_score: int
    verified_score: int
    adjustment_reason: str


class VerificationResult(BaseModel):
    verifications: list[ScoringVerification]


class ImprovementPoint(BaseModel):
    priority: int
    title: str
    why: str
    how: str
    example_rewrite: str


class CoachingResult(BaseModel):
    improvements: list[ImprovementPoint]
    rewrite_30sec_executive: str
    rewrite_2min_engineer: str
    rewrite_doc_summary: str


# --- API Request / Response ---


class EvaluateRequest(BaseModel):
    transcript: str = Field(min_length=10, description="평가할 트랜스크립트 텍스트")
    audience: Optional[str] = Field(default=None, description="청중 유형")
    purpose: Optional[str] = Field(default=None, description="발표 목적")
    remove_fillers: bool = Field(default=True, description="군더더기 제거 여부")
    format: Optional[str] = Field(default=None, description="입력 형식: plain | vtt (미지정 시 자동 감지)")


class CheckpointItem(BaseModel):
    axis: str
    checkpoint: str
    max_score: int = 5
    earned: int
    evidence_quotes: list[EvidenceQuote] = Field(default_factory=list)
    fix: str = ""


class DerivedMetrics(BaseModel):
    numeric_sentence_ratio: float
    vagueness_index: float
    logic_marker_ratio: float


class Rewrites(BaseModel):
    sec30_executive: str = Field(alias="30sec_executive", default="")
    min2_engineer: str = Field(alias="2min_engineer", default="")
    doc_summary: str = ""

    model_config = {"populate_by_name": True}


class ScoreSummary(BaseModel):
    total: int
    purpose_clarity: int
    structure: int
    evidence_specificity: int
    audience_fit: int
    logical_coherence: int
    decision_support: int


class EvaluateMeta(BaseModel):
    version: str = "EQI-v1"
    audience: str = ""
    intent: str = ""
    language: str = "ko"
    processed_at: str = ""


class EvaluateResponse(BaseModel):
    id: Optional[str] = None
    meta: EvaluateMeta
    scores: ScoreSummary
    checkpoint_breakdown: list[CheckpointItem]
    derived_metrics: DerivedMetrics
    improvement_points: list[ImprovementPoint]
    rewrites: Rewrites


# --- Multi-Speaker Models ---


class SpeakerContribution(BaseModel):
    speaker: str
    utterance_count: int = 0
    word_count: int = 0
    speaking_ratio: float = Field(default=0, ge=0, le=1, description="발화 비율 0~1")
    role_summary: str = Field(default="", description="역할 요약 (LLM 생성)")


class MultiSpeakerResponse(BaseModel):
    id: Optional[str] = None
    speakers: list[str]
    contributions: list[SpeakerContribution]
    evaluations: dict[str, EvaluateResponse]


# --- List ---


class EvaluationListItem(BaseModel):
    id: str
    created_at: str
    intent: str
    audience: str
    total_score: int
    transcript_preview: str
