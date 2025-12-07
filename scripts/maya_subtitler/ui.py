"""
Simple UI for creating subtitle locators.

Usage:
    from maya_subtitler import ui
    ui.show()
"""

import maya.cmds as cmds


WINDOW_NAME = "subtitleLocatorWindow"
WINDOW_TITLE = "Subtitle Locator"


def show():
    """Show the subtitle locator UI window."""
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    window = cmds.window(
        WINDOW_NAME,
        title=WINDOW_TITLE,
        widthHeight=(400, 300),
        sizeable=True,
    )

    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=("both", 10))

    cmds.separator(height=10, style="none")

    # Name
    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(100, 280),
        columnAlign1="right",
        adjustableColumn=2,
    )
    cmds.text(label="Name:", width=100, align="right")
    cmds.textField("subtitleNameField", text="subtitleLocator1")
    cmds.setParent("..")

    # Subtitle File
    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(100, 230, 50),
        columnAlign1="right",
        adjustableColumn=2,
    )
    cmds.text(label="SRT File:", width=100, align="right")
    cmds.textField("subtitleFileField", text="")
    cmds.button(label="...", command=lambda x: _browse_file())
    cmds.setParent("..")

    cmds.separator(height=10, style="in")

    # Start Frame
    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(100, 280),
        columnAlign1="right",
        adjustableColumn=2,
    )
    cmds.text(label="Start Frame:", width=100, align="right")
    cmds.intField("startFrameField", value=0, minValue=0, step=1)
    cmds.setParent("..")

    # Font Size
    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=(100, 280),
        columnAlign1="right",
        adjustableColumn=2,
    )
    cmds.text(label="Font Size:", width=100, align="right")
    cmds.intField("fontSizeField", value=18, minValue=8, maxValue=72, step=1)
    cmds.setParent("..")

    cmds.separator(height=10, style="in")

    # Position
    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(100, 140, 140),
        columnAlign1="right",
        adjustableColumn=2,
    )
    cmds.text(label="Position:", width=100, align="right")
    cmds.floatField(
        "positionXField", value=0.0, minValue=-1.0, maxValue=1.0, precision=2, step=0.1
    )
    cmds.floatField(
        "positionYField", value=-0.4, minValue=-1.0, maxValue=1.0, precision=2, step=0.1
    )
    cmds.setParent("..")

    cmds.separator(height=10, style="in")

    # Text Wrapping
    cmds.rowLayout(
        numberOfColumns=3, columnWidth3=(100, 140, 140), columnAlign1="right"
    )
    cmds.text(label="Wrapping:", width=100, align="right")
    cmds.checkBox("wrapTextCheck", label="Enable", value=True)
    cmds.checkBox("wordWrapCheck", label="Word Wrap", value=True)
    cmds.setParent("..")

    cmds.rowLayout(
        numberOfColumns=3,
        columnWidth3=(100, 140, 140),
        columnAlign1="right",
        adjustableColumn=2,
    )
    cmds.text(label="Max Chars:", width=100, align="right")
    cmds.intField("maxCharsField", value=80, minValue=10, maxValue=200, step=1)
    cmds.intField("maxLinesField", value=3, minValue=1, maxValue=10, step=1)
    cmds.setParent("..")

    cmds.separator(height=15, style="none")

    # Create Button
    cmds.button(label="Create", command=lambda x: _create_locator(), height=30)

    cmds.separator(height=10, style="none")

    cmds.showWindow(window)


def _browse_file():
    """Open file browser for SRT file selection."""
    result = cmds.fileDialog2(
        fileMode=1,
        caption="Select SRT File",
        fileFilter="SRT Files (*.srt);;All Files (*.*)",
    )
    if result:
        cmds.textField("subtitleFileField", edit=True, text=result[0])


def _create_locator():
    """Create subtitle locator with current UI settings."""
    # Check if SRT file is set
    subtitle_file = cmds.textField("subtitleFileField", query=True, text=True)
    if not subtitle_file:
        cmds.warning("SRT file is not set.")
        return

    # Ensure plugins are loaded
    from . import load_plugins

    try:
        load_plugins()
    except Exception as e:
        cmds.warning(f"Failed to load plugins: {e}")
        return

    # Get values from UI
    name = cmds.textField("subtitleNameField", query=True, text=True)
    start_frame = cmds.intField("startFrameField", query=True, value=True)
    font_size = cmds.intField("fontSizeField", query=True, value=True)
    position_x = cmds.floatField("positionXField", query=True, value=True)
    position_y = cmds.floatField("positionYField", query=True, value=True)
    wrap_text = cmds.checkBox("wrapTextCheck", query=True, value=True)
    word_wrap = cmds.checkBox("wordWrapCheck", query=True, value=True)
    max_chars = cmds.intField("maxCharsField", query=True, value=True)
    max_lines = cmds.intField("maxLinesField", query=True, value=True)

    # Build command arguments
    kwargs = {
        "name": name,
        "subtitleFile": subtitle_file,
        "startFrame": start_frame,
        "fontSize": font_size,
        "positionX": position_x,
        "positionY": position_y,
        "wrapText": wrap_text,
        "wordWrap": word_wrap,
        "maxCharsPerLine": max_chars,
        "maxLines": max_lines,
    }

    # Create the locator
    result = cmds.createSubtitleLocator(**kwargs)
    cmds.select(result)
    print(f"Created: {result}")
