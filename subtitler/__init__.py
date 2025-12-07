"""Subtitler - Audio transcription and subtitle generation tool."""

__version__ = "1.0.0"

from .transcribe import load_model, transcribe_audio, translate_audio
from .romanize import create_converter, to_romaji, romanize_segments
from .srt import parse_srt, write_srt

__all__ = [
    "load_model",
    "transcribe_audio",
    "translate_audio",
    "create_converter",
    "to_romaji",
    "romanize_segments",
    "parse_srt",
    "write_srt",
]
