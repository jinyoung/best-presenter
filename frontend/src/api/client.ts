import axios from 'axios'
import type { EvaluateRequest, EvaluateResponse, EvaluationListItem, EvaluationResult } from '../types/evaluation'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000, // Multi-speaker LLM calls can be slow
})

export async function postEvaluate(request: EvaluateRequest): Promise<EvaluationResult> {
  const { data } = await api.post<EvaluationResult>('/evaluate', request)
  return data
}

export async function getEvaluations(limit = 20): Promise<EvaluationListItem[]> {
  const { data } = await api.get<EvaluationListItem[]>('/evaluations', { params: { limit } })
  return data
}

export async function getEvaluation(id: string): Promise<{ id: string; created_at: string; result: EvaluateResponse }> {
  const { data } = await api.get(`/evaluations/${id}`)
  return data
}

// --- Settings ---
export interface SettingsResponse {
  api_key_set: boolean
  api_key_masked: string
  model: string
}

export async function getSettings(): Promise<SettingsResponse> {
  const { data } = await api.get<SettingsResponse>('/settings')
  return data
}

export async function saveSettings(body: { api_key?: string; model?: string }): Promise<SettingsResponse> {
  const { data } = await api.post<SettingsResponse>('/settings', body)
  return data
}
