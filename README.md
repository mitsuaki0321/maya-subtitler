# Subtitler

A tool to generate SRT subtitle files from audio files.

**[日本語版 / Japanese](README_JP.md)** | **[Maya Plugin](README_MAYA.md)** | **[Maya Plugin (日本語)](README_MAYA_JP.md)**

## Features

- **Japanese Transcription**: Generate Japanese subtitles from Japanese audio
- **English Transcription**: Generate English subtitles from English audio
- **English Translation**: Generate English translation subtitles from Japanese audio
- **Romaji Conversion**: Convert Japanese subtitles to Romaji

## Requirements

- Python 3.12 or higher
- CUDA-compatible GPU (recommended)

## Installation

```bash
# Using uv
uv sync

# Using pip
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
```

### For GPU (CUDA) Support

PyTorch must be installed separately according to your CUDA version:

```bash
# Example: For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Usage

### GUI

```bash
subtitler-gui
# or
uv run python -m subtitler.gui
```

### CLI

```bash
# Japanese audio � Japanese subtitles
subtitler ja audio.mp3

# Japanese audio � Japanese subtitles + English translation
subtitler ja audio.mp3 --with-english

# English audio � English subtitles
subtitler en audio.mp3

# Japanese subtitles � Romaji subtitles
subtitler romaji subtitle_ja.srt
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output directory | `output` |
| `-m, --model` | Whisper model size (tiny/base/small/medium/large) | `base` |
| `--with-english` | Also generate English translation (ja command only) | - |

## Output Files

| Command | Output Files |
|---------|--------------|
| `ja` | `{filename}_ja.srt` |
| `ja --with-english` | `{filename}_ja.srt`, `{filename}_en.srt` |
| `en` | `{filename}_en.srt` |
| `romaji` | `{filename}_romaji.srt` |

## Whisper Models

| Model | Parameters | Required VRAM | Accuracy |
|-------|------------|---------------|----------|
| tiny | 39M | ~1GB | Low |
| base | 74M | ~1GB | Medium |
| small | 244M | ~2GB | Medium-High |
| medium | 769M | ~5GB | High |
| large | 1550M | ~10GB | Highest |

### Model Storage Location

Models are automatically downloaded on first use and stored in the following locations:

| OS | Path |
|----|------|
| Windows | `C:\Users\<username>\.cache\whisper\` |
| macOS / Linux | `~/.cache/whisper/` |

If the `XDG_CACHE_HOME` environment variable is set, models are stored in `$XDG_CACHE_HOME/whisper/`.

## License

MIT License
