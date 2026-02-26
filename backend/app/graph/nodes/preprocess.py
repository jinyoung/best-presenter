from app.models.state import PipelineState
from app.utils.text import normalize_whitespace, remove_fillers, split_sentences


def preprocess(state: PipelineState) -> dict:
    text = state["transcript"]

    if state.get("remove_fillers", True):
        text = remove_fillers(text)

    text = normalize_whitespace(text)
    sentences = split_sentences(text)

    return {
        "cleaned_text": text,
        "sentences": sentences,
    }
