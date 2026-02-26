from __future__ import annotations

import re

NUMERIC_PATTERN = re.compile(r'\d+(\.\d+)?(%|건|개|명|원|달러|시간|분|초|배|MB|GB|ms|KB)')
VAGUE_WORDS = re.compile(r'\b(많이|상당히|꽤|약간|조금|대략|거의|아마|어느정도|상당한|다소|좀|좋은|나쁜|큰|작은)\b')
LOGIC_MARKERS = re.compile(r'\b(따라서|그러므로|왜냐하면|때문에|결과적으로|반면|그러나|하지만|또한|첫째|둘째|셋째|결론적으로|요약하면|정리하면|먼저|다음으로|마지막으로)\b')


def numeric_sentence_ratio(sentences: list[str]) -> float:
    if not sentences:
        return 0.0
    count = sum(1 for s in sentences if NUMERIC_PATTERN.search(s))
    return round(count / len(sentences), 3)


def vagueness_index(sentences: list[str]) -> float:
    if not sentences:
        return 0.0
    total_words = sum(len(s.split()) for s in sentences)
    if total_words == 0:
        return 0.0
    vague_count = sum(len(VAGUE_WORDS.findall(s)) for s in sentences)
    return round(vague_count / total_words, 3)


def logic_marker_ratio(sentences: list[str]) -> float:
    if not sentences:
        return 0.0
    count = sum(1 for s in sentences if LOGIC_MARKERS.search(s))
    return round(count / len(sentences), 3)


def compute_all_metrics(sentences: list[str]) -> dict[str, float]:
    return {
        "numeric_sentence_ratio": numeric_sentence_ratio(sentences),
        "vagueness_index": vagueness_index(sentences),
        "logic_marker_ratio": logic_marker_ratio(sentences),
    }
