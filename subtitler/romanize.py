"""Japanese to Romaji conversion."""

import pykakasi


def create_converter() -> pykakasi.kakasi:
    """Create and configure pykakasi converter."""
    kks = pykakasi.kakasi()
    kks.setMode("H", "a")  # Hiragana to ascii
    kks.setMode("K", "a")  # Katakana to ascii
    kks.setMode("J", "a")  # Japanese to ascii
    kks.setMode("s", True)  # Add spaces between words
    return kks


def to_romaji(text: str, converter: pykakasi.kakasi | None = None) -> str:
    """Convert Japanese text to romaji.

    Args:
        text: Japanese text to convert
        converter: Optional pykakasi instance (creates new one if None)

    Returns:
        Romanized text
    """
    if converter is None:
        converter = create_converter()
    conv = converter.getConverter()
    return conv.do(text)


def romanize_segments(
    segments: list[dict], converter: pykakasi.kakasi | None = None
) -> list[dict]:
    """Convert Japanese segments to romaji.

    Args:
        segments: List of dicts with 'start', 'end', 'text' keys
        converter: Optional pykakasi instance

    Returns:
        New list of segments with romanized text
    """
    if converter is None:
        converter = create_converter()

    result = []
    for seg in segments:
        result.append(
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": to_romaji(seg["text"], converter),
            }
        )
    return result
