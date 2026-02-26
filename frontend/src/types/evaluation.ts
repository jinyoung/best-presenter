export interface EvidenceQuote {
  text: string
  loc: string
  sentiment: 'positive' | 'negative'
}

export interface CheckpointItem {
  axis: string
  checkpoint: string
  max_score: number
  earned: number
  evidence_quotes: EvidenceQuote[]
  fix: string
}

export interface DerivedMetrics {
  numeric_sentence_ratio: number
  vagueness_index: number
  logic_marker_ratio: number
}

export interface ImprovementPoint {
  priority: number
  title: string
  why: string
  how: string
  example_rewrite: string
}

export interface Rewrites {
  '30sec_executive': string
  '2min_engineer': string
  doc_summary: string
}

export interface ScoreSummary {
  total: number
  purpose_clarity: number
  structure: number
  evidence_specificity: number
  audience_fit: number
  logical_coherence: number
  decision_support: number
}

export interface EvaluateMeta {
  version: string
  audience: string
  intent: string
  language: string
  processed_at: string
}

export interface EvaluateResponse {
  id?: string
  meta: EvaluateMeta
  scores: ScoreSummary
  checkpoint_breakdown: CheckpointItem[]
  derived_metrics: DerivedMetrics
  improvement_points: ImprovementPoint[]
  rewrites: Rewrites
}

export interface EvaluateRequest {
  transcript: string
  audience?: string
  purpose?: string
  remove_fillers?: boolean
  format?: 'plain' | 'vtt'
}

export interface SpeakerContribution {
  speaker: string
  utterance_count: number
  word_count: number
  speaking_ratio: number
  role_summary: string
}

export interface MultiSpeakerResponse {
  id?: string
  speakers: string[]
  contributions: SpeakerContribution[]
  evaluations: Record<string, EvaluateResponse>
}

export type EvaluationResult = EvaluateResponse | MultiSpeakerResponse

export function isMultiSpeaker(result: EvaluationResult): result is MultiSpeakerResponse {
  return 'speakers' in result && 'evaluations' in result
}

export interface EvaluationListItem {
  id: string
  created_at: string
  intent: string
  audience: string
  total_score: number
  transcript_preview: string
}

export const AXIS_LABELS: Record<string, string> = {
  purpose_clarity: '목적 명확성',
  structure: '구조',
  evidence_specificity: '근거 구체성',
  audience_fit: '청중 적합성',
  logical_coherence: '논리 일관성',
  decision_support: '의사결정 지원',
}

export const AXES = [
  'purpose_clarity',
  'structure',
  'evidence_specificity',
  'audience_fit',
  'logical_coherence',
  'decision_support',
] as const
