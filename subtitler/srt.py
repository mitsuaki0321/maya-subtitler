"""SRT file utilities."""

import re
from pathlib import Path


def parse_timestamp(timestamp: str) -> float:
    """Parse SRT timestamp to seconds.

    Args:
        timestamp: SRT format timestamp (HH:MM:SS,mmm)

    Returns:
        Time in seconds
    """
    match = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", timestamp)
    if not match:
        return 0.0

    hours, minutes, seconds, millis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def parse_srt(srt_path: Path) -> list[dict]:
    """Parse SRT file to list of segments.

    Args:
        srt_path: Path to SRT file

    Returns:
        List of dicts with 'start', 'end', 'text' keys
    """
    segments = []

    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by double newlines (segment separator)
    blocks = re.split(r"\n\n+", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        # Line 0: index (ignored)
        # Line 1: timestamp
        # Line 2+: text
        timestamp_line = lines[1]
        text_lines = lines[2:]

        # Parse timestamp
        match = re.match(r"(.+?)\s*-->\s*(.+)", timestamp_line)
        if not match:
            continue

        start_str, end_str = match.groups()
        start = parse_timestamp(start_str.strip())
        end = parse_timestamp(end_str.strip())
        text = " ".join(text_lines)

        segments.append({"start": start, "end": end, "text": text})

    return segments


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(segments: list[dict], output_path: Path) -> None:
    """Write segments to SRT file.

    Args:
        segments: List of dicts with 'start', 'end', 'text' keys
        output_path: Path to output SRT file
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
