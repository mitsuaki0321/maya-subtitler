# Subtitler

音声ファイルから SRT 字幕ファイルを生成するツールです。

**[English](README.md)** | **[Maya Plugin](README_MAYA.md)** | **[Maya Plugin (日本語)](README_MAYA_JP.md)**

## 機能

- **日本語文字起こし**: 日本語音声から日本語字幕を生成
- **英語文字起こし**: 英語音声から英語字幕を生成
- **英語翻訳**: 日本語音声から英語翻訳字幕を生成
- **ローマ字変換**: 日本語字幕をローマ字に変換

## 必要環境

- Python 3.12 以上
- CUDA 対応 GPU（推奨）

## インストール

```bash
# uv を使う場合
uv sync

# pip を使う場合
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
```

### GPU (CUDA) を使用する場合

PyTorch は CUDA バージョンに応じて別途インストールが必要です:

```bash
# 例: CUDA 12.1 の場合
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## 使用方法

### GUI

```bash
subtitler-gui
# または
uv run python -m subtitler.gui
```

### CLI

```bash
# 日本語音声 -> 日本語字幕
subtitler ja audio.mp3

# 日本語音声 -> 日本語字幕 + 英語翻訳
subtitler ja audio.mp3 --with-english

# 英語音声 -> 英語字幕
subtitler en audio.mp3

# 日本語字幕 -> ローマ字字幕
subtitler romaji subtitle_ja.srt
```

### オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `-o, --output` | 出力ディレクトリ | `output` |
| `-m, --model` | Whisper モデルサイズ (tiny/base/small/medium/large) | `base` |
| `--with-english` | 英語翻訳も生成 (ja コマンドのみ) | - |

## 出力ファイル

| コマンド | 出力ファイル |
|---------|-------------|
| `ja` | `{filename}_ja.srt` |
| `ja --with-english` | `{filename}_ja.srt`, `{filename}_en.srt` |
| `en` | `{filename}_en.srt` |
| `romaji` | `{filename}_romaji.srt` |

## Whisper モデル

| モデル | パラメータ数 | 必要 VRAM | 精度 |
|-------|------------|----------|------|
| tiny | 39M | ~1GB | 低 |
| base | 74M | ~1GB | 中 |
| small | 244M | ~2GB | 中高 |
| medium | 769M | ~5GB | 高 |
| large | 1550M | ~10GB | 最高 |

### モデルの保存場所

モデルは初回使用時に自動でダウンロードされ、以下の場所に保存されます:

| OS | パス |
|----|------|
| Windows | `C:\Users\<ユーザー名>\.cache\whisper\` |
| macOS / Linux | `~/.cache/whisper/` |

環境変数 `XDG_CACHE_HOME` が設定されている場合は `$XDG_CACHE_HOME/whisper/` に保存されます。

## ライセンス

MIT License
