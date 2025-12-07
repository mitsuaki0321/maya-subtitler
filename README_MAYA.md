# Maya Subtitler

A Maya plugin to display subtitles in the viewport. Reads SRT files and displays subtitles synchronized with the timeline.

**[日本語版 / Japanese](README_MAYA_JP.md)** | **[Subtitler (Audio Tool)](README.md)** | **[Subtitler (日本語)](README_JP.md)**

## Features

- Direct SRT file loading
- Timeline-synchronized display
- Per-camera display control (via message attribute connection)
- Customizable font size, color, and position
- Text wrapping (character-based or word-based)
- Viewport 2.0 support

## Installation

### Module Method (Recommended)

1. Clone this repository to any location
2. Add the path to `maya_subtitler.mod` to Maya's module path

**Method A**: Set environment variable
```
MAYA_MODULE_PATH=C:\path\to\maya-subtitler
```

**Method B**: Copy to Maya's modules folder
```
# Windows
%USERPROFILE%\Documents\maya\modules\maya_subtitler.mod

# macOS / Linux
~/maya/modules/maya_subtitler.mod
```

### Manual Installation

1. `plug-ins/subtitleLocator.py` -> Maya's plug-ins folder
2. `scripts/maya_subtitler/` -> Maya's scripts folder
3. `scripts/AEsubtitleLocatorTemplate.mel` -> Maya's scripts folder

## Usage

### From Python

```python
import maya_subtitler
maya_subtitler.show_ui()
```

### UI

1. **Name**: Locator name
2. **SRT File**: Path to subtitle file
3. **Start Frame**: Starting frame for subtitles (position on timeline)
4. **Font Size**: Font size
5. **Position**: Screen position (X: horizontal, Y: vertical)
6. **Wrapping**: Text wrapping settings
   - Enable: Enable text wrapping
   - Word Wrap: Wrap by words (character-based recommended for Japanese)
7. **Max Chars / Max Lines**: Maximum characters per line and maximum lines

### From Command

```python
import maya.cmds as cmds

# Load plugin
cmds.loadPlugin("subtitleLocator")

# Create locator
cmds.createSubtitleLocator(
    name="mySubtitle",
    subtitleFile="C:/path/to/subtitle.srt",
    startFrame=0,
    fontSize=24,
    positionX=0.0,
    positionY=-0.4,
)
```

## Attributes

| Attribute | Type | Description | Default |
|-----------|------|-------------|---------|
| `subtitleFile` | string | SRT file path | - |
| `targetCamera` | message | Target camera (connection) | - |
| `startFrame` | int | Start frame | 0 |
| `fontSize` | int | Font size | 18 |
| `fontColor` | float3 | Font color (RGB) | (1, 1, 1) |
| `positionX` | float | Horizontal position (-1 to 1) | 0.0 |
| `positionY` | float | Vertical position (-1 to 1) | -0.4 |
| `wrapText` | bool | Enable wrapping | true |
| `wordWrap` | bool | Wrap by words | true |
| `maxCharsPerLine` | int | Max characters per line | 80 |
| `maxLines` | int | Max lines | 3 |

## Camera Connection

To display subtitles only in a specific camera, connect the camera shape's message attribute:

```python
cmds.connectAttr("perspShape.message", "subtitleLocatorShape1.targetCamera")
```

If no connection is made, subtitles are displayed in all cameras.

## Multiple Language Subtitles

To display subtitles in different languages, create multiple locators and toggle visibility:

```python
# Japanese subtitles
cmds.createSubtitleLocator(name="subtitle_ja", subtitleFile="movie_ja.srt")

# English subtitles
cmds.createSubtitleLocator(name="subtitle_en", subtitleFile="movie_en.srt")
cmds.setAttr("subtitle_en.visibility", 0)  # Hide
```

## Supported Maya Versions

- Maya 2022 and later (Python 3, Viewport 2.0 support)

## License

MIT License
