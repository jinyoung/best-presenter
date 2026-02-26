from __future__ import annotations

from datetime import datetime, timezone

from app.models.schemas import (
    CheckpointItem,
    DerivedMetrics,
    EvaluateMeta,
    EvaluateResponse,
    EvidenceQuote,
    Rewrites,
    ScoreSummary,
)
from app.models.state import PipelineState


def compose(state: PipelineState) -> dict:
    classification = state["classification"]
    axis_scores = state["final_axis_scores"]
    scoring = state["scoring"]
    evidence = state["evidence"]
    coaching = state["coaching"]
    derived = state["derived_metrics"]
    verification = state["verification"]

    # Build verified scores lookup
    verified = {}
    for v in verification.verifications:
        verified[(v.axis, v.checkpoint)] = v.verified_score

    # Total score = weighted average of axis scores
    if axis_scores:
        total = round(sum(axis_scores.values()) / len(axis_scores))
    else:
        total = 0

    # Build meta
    meta = EvaluateMeta(
        version="EQI-v1",
        audience=classification.audience_level,
        intent=classification.intent,
        language="ko",
        processed_at=datetime.now(timezone.utc).isoformat(),
    )

    # Build scores summary
    scores = ScoreSummary(
        total=total,
        purpose_clarity=axis_scores.get("purpose_clarity", 0),
        structure=axis_scores.get("structure", 0),
        evidence_specificity=axis_scores.get("evidence_specificity", 0),
        audience_fit=axis_scores.get("audience_fit", 0),
        logical_coherence=axis_scores.get("logical_coherence", 0),
        decision_support=axis_scores.get("decision_support", 0),
    )

    # Build checkpoint breakdown
    evidence_map: dict[tuple[str, str], list[EvidenceQuote]] = {}
    for axis_ev in evidence.axes:
        for cp_ev in axis_ev.checkpoints:
            quotes = []
            for q in cp_ev.positive:
                quotes.append(EvidenceQuote(text=q.text, loc=q.loc, sentiment="positive"))
            for q in cp_ev.negative:
                quotes.append(EvidenceQuote(text=q.text, loc=q.loc, sentiment="negative"))
            evidence_map[(axis_ev.axis, cp_ev.checkpoint)] = quotes

    breakdown = []
    for axis_s in scoring.axes:
        for cp_s in axis_s.checkpoints:
            earned = verified.get((axis_s.axis, cp_s.checkpoint), cp_s.earned)
            quotes = evidence_map.get((axis_s.axis, cp_s.checkpoint), [])
            fix = cp_s.reasoning if earned <= 2 else ""
            breakdown.append(CheckpointItem(
                axis=axis_s.axis,
                checkpoint=cp_s.checkpoint,
                max_score=cp_s.max_score,
                earned=earned,
                evidence_quotes=quotes,
                fix=fix,
            ))

    # Build rewrites
    rewrites = Rewrites(**{
        "30sec_executive": coaching.rewrite_30sec_executive,
        "2min_engineer": coaching.rewrite_2min_engineer,
        "doc_summary": coaching.rewrite_doc_summary,
    })

    response = EvaluateResponse(
        meta=meta,
        scores=scores,
        checkpoint_breakdown=breakdown,
        derived_metrics=derived,
        improvement_points=coaching.improvements,
        rewrites=rewrites,
    )

    return {"response": response}
