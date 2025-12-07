"""Audio transcription using Whisper."""

from pathlib import Path

import whisper

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
MODELS_DIR = PROJECT_ROOT / "models"


def load_model(
    model_name: str = "base", download_root: Path | None = None
) -> whisper.Whisper:
    """Load Whisper model.

    Args:
        model_name: Model size - tiny, base, small, medium, large
        download_root: Directory to save/load models (default: PROJECT/models)

    Returns:
        Loaded Whisper model
    """
    if download_root is None:
        download_root = MODELS_DIR
    download_root.mkdir(parents=True, exist_ok=True)
    return whisper.load_model(model_name, download_root=str(download_root))


def transcribe_audio(
    audio_path: Path,
    model: whisper.Whisper,
    language: str = "ja",
) -> list[dict]:
    """Transcribe audio file to Japanese text.

    Args:
        audio_path: Path to audio file (mp3, wav)
        model: Loaded Whisper model
        language: Source language code

    Returns:
        List of segments with 'start', 'end', 'text' keys
    """
    result = model.transcribe(
        str(audio_path),
        language=language,
        task="transcribe",
    )
    return result["segments"]


def translate_audio(
    audio_path: Path,
    model: whisper.Whisper,
    language: str = "ja",
) -> list[dict]:
    """Translate audio to English text.

    Args:
        audio_path: Path to audio file (mp3, wav)
        model: Loaded Whisper model
        language: Source language code

    Returns:
        List of segments with 'start', 'end', 'text' keys
    """
    result = model.transcribe(
        str(audio_path),
        language=language,
        task="translate",
    )
    return result["segments"]
