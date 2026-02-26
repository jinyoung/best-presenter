from __future__ import annotations

import re
from dataclasses import dataclass, field


# --- VTT Parsing ---


@dataclass
class SpeakerSegment:
    speaker: str
    text: str
    start_time: str
    end_time: str


_TIMESTAMP_RE = re.compile(
    r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})"
)
_SPEAKER_RE = re.compile(r"^([^:]+):\s*(.+)$")


def is_vtt(text: str) -> bool:
    """Detect whether text looks like a VTT transcript."""
    return bool(_TIMESTAMP_RE.search(text))


def parse_vtt(vtt_text: str) -> list[SpeakerSegment]:
    """Parse VTT text into a list of SpeakerSegments.

    Expected format per cue:
        1
        00:00:00.000 --> 00:00:05.000
        SPEAKER: some text
    """
    segments: list[SpeakerSegment] = []
    lines = vtt_text.strip().splitlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip WEBVTT header and blank lines
        if not line or line.startswith("WEBVTT") or line.startswith("NOTE"):
            i += 1
            continue

        # Skip cue index numbers (pure digits)
        if line.isdigit():
            i += 1
            continue

        # Look for timestamp line
        ts_match = _TIMESTAMP_RE.match(line)
        if ts_match:
            start_time = ts_match.group(1)
            end_time = ts_match.group(2)

            # Collect all text lines until next blank line or timestamp
            i += 1
            text_lines: list[str] = []
            while i < len(lines) and lines[i].strip() and not _TIMESTAMP_RE.match(lines[i].strip()) and not lines[i].strip().isdigit():
                text_lines.append(lines[i].strip())
                i += 1

            full_text = " ".join(text_lines)
            speaker_match = _SPEAKER_RE.match(full_text)

            if speaker_match:
                speaker = speaker_match.group(1).strip()
                text = speaker_match.group(2).strip()
            else:
                speaker = "Unknown"
                text = full_text.strip()

            if text:
                segments.append(SpeakerSegment(
                    speaker=speaker,
                    text=text,
                    start_time=start_time,
                    end_time=end_time,
                ))
        else:
            i += 1

    return segments


def group_by_speaker(segments: list[SpeakerSegment]) -> dict[str, str]:
    """Group all segments by speaker, concatenating their text."""
    groups: dict[str, list[str]] = {}
    for seg in segments:
        groups.setdefault(seg.speaker, []).append(seg.text)
    return {speaker: " ".join(texts) for speaker, texts in groups.items()}


# --- Text Utilities ---


FILLER_PATTERNS = [
    r'\b(음+|어+|그+|아+|에+)\b',
    r'\.{2,}',
    r'\b(그러니까|뭐랄까|있잖아|저기|이제)\b',
]

FILLER_RE = re.compile('|'.join(FILLER_PATTERNS), re.IGNORECASE)


def remove_fillers(text: str) -> str:
    result = FILLER_RE.sub('', text)
    return normalize_whitespace(result)


def split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?。])\s+', text.strip())
    sentences = [s.strip() for s in parts if s.strip()]
    return sentences


def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()
