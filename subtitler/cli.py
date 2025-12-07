"""Subtitler - Command line interface."""

import argparse
import sys
from pathlib import Path

from .transcribe import load_model, transcribe_audio, translate_audio
from .romanize import romanize_segments, create_converter
from .srt import write_srt, parse_srt


def cmd_ja(args):
    """Japanese audio to Japanese SRT (optionally with English)."""
    if not args.audio.exists():
        print(f"Error: Audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = args.audio.stem

    print(f"Loading Whisper model: {args.model}")
    model = load_model(args.model)

    # Japanese transcription
    print("Transcribing Japanese...")
    ja_segments = transcribe_audio(args.audio, model, language="ja")
    ja_srt_path = output_dir / f"{base_name}_ja.srt"
    write_srt(ja_segments, ja_srt_path)
    print(f"  -> {ja_srt_path}")

    # Optional English translation
    if args.with_english:
        print("Translating to English...")
        en_segments = translate_audio(args.audio, model, language="ja")
        en_srt_path = output_dir / f"{base_name}_en.srt"
        write_srt(en_segments, en_srt_path)
        print(f"  -> {en_srt_path}")

    print("Done!")


def cmd_en(args):
    """English audio to English SRT."""
    if not args.audio.exists():
        print(f"Error: Audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = args.audio.stem

    print(f"Loading Whisper model: {args.model}")
    model = load_model(args.model)

    # English transcription
    print("Transcribing English...")
    en_segments = transcribe_audio(args.audio, model, language="en")
    en_srt_path = output_dir / f"{base_name}_en.srt"
    write_srt(en_segments, en_srt_path)
    print(f"  -> {en_srt_path}")

    print("Done!")


def cmd_romaji(args):
    """Convert Japanese SRT to Romaji SRT."""
    if not args.srt.exists():
        print(f"Error: SRT file not found: {args.srt}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = args.srt.stem

    # Remove _ja suffix if present
    if base_name.endswith("_ja"):
        base_name = base_name[:-3]

    print("Loading SRT file...")
    ja_segments = parse_srt(args.srt)

    print("Converting to Romaji...")
    converter = create_converter()
    romaji_segments = romanize_segments(ja_segments, converter)
    romaji_srt_path = output_dir / f"{base_name}_romaji.srt"
    write_srt(romaji_segments, romaji_srt_path)
    print(f"  -> {romaji_srt_path}")

    print("Done!")


def main():
    parser = argparse.ArgumentParser(
        description="Subtitler - Transcription and subtitle generation"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Japanese command
    ja_parser = subparsers.add_parser("ja", help="Transcribe Japanese audio to SRT")
    ja_parser.add_argument("audio", type=Path, help="Path to audio file (mp3, wav)")
    ja_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output"),
        help="Output directory (default: output)",
    )
    ja_parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)",
    )
    ja_parser.add_argument(
        "--with-english",
        action="store_true",
        help="Also generate English translation",
    )
    ja_parser.set_defaults(func=cmd_ja)

    # English command
    en_parser = subparsers.add_parser("en", help="Transcribe English audio to SRT")
    en_parser.add_argument("audio", type=Path, help="Path to audio file (mp3, wav)")
    en_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output"),
        help="Output directory (default: output)",
    )
    en_parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)",
    )
    en_parser.set_defaults(func=cmd_en)

    # Romaji command
    romaji_parser = subparsers.add_parser(
        "romaji", help="Convert Japanese SRT to Romaji"
    )
    romaji_parser.add_argument("srt", type=Path, help="Path to Japanese SRT file")
    romaji_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output"),
        help="Output directory (default: output)",
    )
    romaji_parser.set_defaults(func=cmd_romaji)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
