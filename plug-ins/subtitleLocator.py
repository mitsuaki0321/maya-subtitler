"""
Subtitle Locator Node for Maya.

A custom locator that displays subtitles synchronized with the timeline.
Reads SRT files directly.

Attributes:
    subtitleFile (string): Path to the SRT file
    targetCamera (message): Camera to display subtitles in (connect camera shape)
    startFrame (int): Frame where subtitle time 0 begins (default: 0)
    fontSize (int): Font size for subtitle display
    fontColor (float3): Font color RGB
    positionX (float): Horizontal position offset (-1 to 1)
    positionY (float): Vertical position offset (-1 to 1)
    wrapText (bool): Enable text wrapping
    wordWrap (bool): Wrap by words (True) or characters (False)
    maxCharsPerLine (int): Maximum characters per line
    maxLines (int): Maximum number of lines
"""

import re
import sys
from pathlib import Path

from maya.api import OpenMaya, OpenMayaAnim, OpenMayaRender, OpenMayaUI


def maya_useNewAPI():
    pass


# Plug-in information
K_PLUGIN_NODE_NAME = "subtitleLocator"
K_PLUGIN_NODE_ID = OpenMaya.MTypeId(0x0007F7F8)
K_PLUGIN_CLASSIFICATION = "drawdb/geometry/subtitleLocator"
K_DRAW_REGISTRANT_ID = "subtitleLocatorNode"

# Default values
DEFAULT_START_FRAME = 0
DEFAULT_FONT_SIZE = 18
DEFAULT_FONT_COLOR = (1.0, 1.0, 1.0)
DEFAULT_POSITION_X = 0.0
DEFAULT_POSITION_Y = -0.4
DEFAULT_WRAP_TEXT = True
DEFAULT_WORD_WRAP = True
DEFAULT_MAX_CHARS_PER_LINE = 80
DEFAULT_MAX_LINES = 3


class SubtitleLocator(OpenMayaUI.MPxLocatorNode):
    """Subtitle locator node."""

    # Attributes
    subtitle_file = None
    target_camera = None
    start_frame = None
    font_size = None
    font_color = None
    position_x = None
    position_y = None
    wrap_text = None
    word_wrap = None
    max_chars_per_line = None
    max_lines = None

    def __init__(self):
        """Constructor."""
        OpenMayaUI.MPxLocatorNode.__init__(self)

    def postConstructor(self):
        """Post constructor."""
        node_fn = OpenMaya.MFnDependencyNode(self.thisMObject())
        node_fn.setName("subtitleLocatorShape#")

    @staticmethod
    def creator():
        """Creator."""
        return SubtitleLocator()

    @staticmethod
    def initialize():
        """Initialize the node attributes."""
        typed_attr = OpenMaya.MFnTypedAttribute()
        numeric_attr = OpenMaya.MFnNumericAttribute()
        message_attr = OpenMaya.MFnMessageAttribute()

        # Subtitle file path (SRT)
        SubtitleLocator.subtitle_file = typed_attr.create(
            "subtitleFile", "sf", OpenMaya.MFnData.kString
        )
        typed_attr.storable = True
        typed_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.subtitle_file)

        # Target camera (message connection)
        SubtitleLocator.target_camera = message_attr.create("targetCamera", "tc")
        message_attr.storable = True
        message_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.target_camera)

        # Start frame (frame where subtitle time 0 begins)
        SubtitleLocator.start_frame = numeric_attr.create(
            "startFrame", "stf", OpenMaya.MFnNumericData.kInt, DEFAULT_START_FRAME
        )
        numeric_attr.setMin(0)
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.start_frame)

        # Font size
        SubtitleLocator.font_size = numeric_attr.create(
            "fontSize", "fs", OpenMaya.MFnNumericData.kInt, DEFAULT_FONT_SIZE
        )
        numeric_attr.setMin(8)
        numeric_attr.setMax(72)
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.font_size)

        # Font color
        SubtitleLocator.font_color = numeric_attr.createColor("fontColor", "fc")
        numeric_attr.default = DEFAULT_FONT_COLOR
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.font_color)

        # Position X (normalized -1 to 1)
        SubtitleLocator.position_x = numeric_attr.create(
            "positionX", "px", OpenMaya.MFnNumericData.kFloat, DEFAULT_POSITION_X
        )
        numeric_attr.setMin(-1.0)
        numeric_attr.setMax(1.0)
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.position_x)

        # Position Y (normalized -1 to 1)
        SubtitleLocator.position_y = numeric_attr.create(
            "positionY", "py", OpenMaya.MFnNumericData.kFloat, DEFAULT_POSITION_Y
        )
        numeric_attr.setMin(-1.0)
        numeric_attr.setMax(1.0)
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.position_y)

        # Wrap text
        SubtitleLocator.wrap_text = numeric_attr.create(
            "wrapText", "wt", OpenMaya.MFnNumericData.kBoolean, DEFAULT_WRAP_TEXT
        )
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.wrap_text)

        # Word wrap (True = word-based, False = character-based)
        SubtitleLocator.word_wrap = numeric_attr.create(
            "wordWrap", "ww", OpenMaya.MFnNumericData.kBoolean, DEFAULT_WORD_WRAP
        )
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.word_wrap)

        # Max characters per line
        SubtitleLocator.max_chars_per_line = numeric_attr.create(
            "maxCharsPerLine",
            "mcpl",
            OpenMaya.MFnNumericData.kInt,
            DEFAULT_MAX_CHARS_PER_LINE,
        )
        numeric_attr.setMin(10)
        numeric_attr.setMax(200)
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.max_chars_per_line)

        # Max lines
        SubtitleLocator.max_lines = numeric_attr.create(
            "maxLines", "ml", OpenMaya.MFnNumericData.kInt, DEFAULT_MAX_LINES
        )
        numeric_attr.setMin(1)
        numeric_attr.setMax(10)
        numeric_attr.keyable = True
        numeric_attr.storable = True
        numeric_attr.writable = True
        SubtitleLocator.addAttribute(SubtitleLocator.max_lines)

    def draw(self, view, path, style, status):
        """Legacy draw - not used."""
        return None


class SubtitleLocatorData(OpenMaya.MUserData):
    """User data for subtitle locator drawing."""

    def __init__(self):
        """Constructor."""
        OpenMaya.MUserData.__init__(self, False)
        self.subtitle_text = ""
        self.font_size = DEFAULT_FONT_SIZE
        self.font_color = OpenMaya.MColor(DEFAULT_FONT_COLOR)
        self.position_x = DEFAULT_POSITION_X
        self.position_y = DEFAULT_POSITION_Y
        self.should_draw = True


class SubtitleLocatorDrawOverride(OpenMayaRender.MPxDrawOverride):
    """Draw override for subtitle locator."""

    # Cache for loaded subtitle data
    _subtitle_cache = {}

    def __init__(self, obj):
        """Constructor."""
        OpenMayaRender.MPxDrawOverride.__init__(
            self, obj, SubtitleLocatorDrawOverride.draw, isAlwaysDirty=True
        )

    @staticmethod
    def creator(obj):
        """Creator."""
        return SubtitleLocatorDrawOverride(obj)

    @staticmethod
    def draw(context, data):
        """Draw callback - not used, we use addUIDrawables."""
        return None

    def supportedDrawAPIs(self):
        """Get supported draw APIs."""
        return (
            OpenMayaRender.MRenderer.kOpenGL
            | OpenMayaRender.MRenderer.kOpenGLCoreProfile
            | OpenMayaRender.MRenderer.kDirectX11
        )

    def hasUIDrawables(self):
        """Enable UI drawables."""
        return True

    def prepareForDraw(self, obj_path, camera_path, frame_context, old_data):
        """Prepare data for drawing."""
        data = old_data
        if not isinstance(data, SubtitleLocatorData):
            data = SubtitleLocatorData()

        node = obj_path.node()
        data.should_draw = True

        # Check target camera
        target_camera_plug = OpenMaya.MPlug(node, SubtitleLocator.target_camera)
        if target_camera_plug.isConnected:
            # Get connected camera
            connections = target_camera_plug.connectedTo(True, False)
            if connections:
                connected_node = connections[0].node()
                # Get the camera shape's full path
                connected_path = OpenMaya.MDagPath.getAPathTo(connected_node)

                # Compare with current camera
                current_camera_path = camera_path.fullPathName()
                target_camera_path = connected_path.fullPathName()

                if current_camera_path != target_camera_path:
                    data.should_draw = False
                    data.subtitle_text = ""
                    return data

        # Get attributes
        data.font_size = OpenMaya.MPlug(node, SubtitleLocator.font_size).asInt()
        data.font_color = OpenMaya.MColor(
            OpenMaya.MPlug(node, SubtitleLocator.font_color).asMDataHandle().asFloat3()
        )
        data.position_x = OpenMaya.MPlug(node, SubtitleLocator.position_x).asFloat()
        data.position_y = OpenMaya.MPlug(node, SubtitleLocator.position_y).asFloat()

        # Get wrap settings
        wrap_text = OpenMaya.MPlug(node, SubtitleLocator.wrap_text).asBool()
        word_wrap = OpenMaya.MPlug(node, SubtitleLocator.word_wrap).asBool()
        max_chars = OpenMaya.MPlug(node, SubtitleLocator.max_chars_per_line).asInt()
        max_lines = OpenMaya.MPlug(node, SubtitleLocator.max_lines).asInt()

        # Get subtitle file path
        subtitle_file_plug = OpenMaya.MPlug(node, SubtitleLocator.subtitle_file)
        subtitle_file = subtitle_file_plug.asString()

        # Get start frame
        start_frame = OpenMaya.MPlug(node, SubtitleLocator.start_frame).asInt()

        # Get current time in frames, then convert to subtitle time in seconds
        current_frame = OpenMayaAnim.MAnimControl.currentTime().value
        fps = OpenMaya.MTime(1.0, OpenMaya.MTime.kSeconds).asUnits(
            OpenMayaAnim.MAnimControl.currentTime().unit
        )

        # Calculate subtitle time: (currentFrame - startFrame) / fps
        subtitle_time = (current_frame - start_frame) / fps

        # Find subtitle for current time
        raw_text = self._get_subtitle_at_time(subtitle_file, subtitle_time)

        # Apply text wrapping if enabled
        if wrap_text and raw_text:
            data.subtitle_text = self._wrap_text(
                raw_text, max_chars, max_lines, word_wrap
            )
        else:
            data.subtitle_text = raw_text

        return data

    def _wrap_text(self, text, max_chars, max_lines, word_wrap):
        """Wrap text according to settings.

        Args:
            text: Original text
            max_chars: Maximum characters per line
            max_lines: Maximum number of lines
            word_wrap: True for word-based, False for character-based

        Returns:
            Wrapped text with newlines
        """
        if not text or len(text) <= max_chars:
            return text

        lines = []

        if not word_wrap:  # Character-based wrapping
            remaining = text
            while remaining and len(lines) < max_lines:
                if len(lines) == max_lines - 1:
                    # Last line - no wrapping
                    lines.append(remaining)
                    break
                else:
                    lines.append(remaining[:max_chars])
                    remaining = remaining[max_chars:]
        else:  # Word-based wrapping
            words = text.split()
            current_line = ""

            for word in words:
                if len(lines) == max_lines - 1:
                    # Last line - add remaining words without wrapping
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                elif len(current_line) + len(word) + 1 <= max_chars:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

        return "\n".join(lines)

    def _get_subtitle_at_time(self, subtitle_file, time_seconds):
        """Get subtitle text for the given time.

        Args:
            subtitle_file: Path to SRT file
            time_seconds: Current time in seconds

        Returns:
            Subtitle text or empty string
        """
        if not subtitle_file:
            return ""

        # Load subtitle data (with caching)
        segments = self._load_srt(subtitle_file)
        if not segments:
            return ""

        # Find subtitle at current time
        for segment in segments:
            start = segment.get("start", 0)
            end = segment.get("end", 0)
            if start <= time_seconds < end:
                return segment.get("text", "")

        return ""

    def _parse_srt_timestamp(self, timestamp):
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

    def _load_srt(self, subtitle_file):
        """Load subtitles from SRT file with caching.

        Args:
            subtitle_file: Path to SRT file

        Returns:
            List of segments or empty list
        """
        # Check cache
        if subtitle_file in self._subtitle_cache:
            return self._subtitle_cache[subtitle_file]

        # Load file
        try:
            path = Path(subtitle_file)
            if not path.exists():
                return []

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse SRT
            segments = []
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
                start = self._parse_srt_timestamp(start_str.strip())
                end = self._parse_srt_timestamp(end_str.strip())
                text = " ".join(text_lines)

                segments.append({"start": start, "end": end, "text": text})

            self._subtitle_cache[subtitle_file] = segments
            return segments

        except Exception as e:
            OpenMaya.MGlobal.displayWarning(f"Failed to load SRT file: {e}")
            return []

    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        """Add UI drawables for subtitle display."""
        if not isinstance(data, SubtitleLocatorData):
            return

        if not data.should_draw or not data.subtitle_text:
            return

        draw_manager.beginDrawable()

        # Get viewport dimensions
        viewport_width = frame_context.getViewportDimensions()[2]
        viewport_height = frame_context.getViewportDimensions()[3]

        # Calculate base position (normalized to pixel coordinates)
        pos_x = int(viewport_width * (0.5 + data.position_x * 0.5))
        pos_y = int(viewport_height * (0.5 + data.position_y * 0.5))

        # Set font properties
        draw_manager.setFontSize(data.font_size)
        draw_manager.setColor(data.font_color)

        # Split text into lines and draw each line separately
        lines = data.subtitle_text.split("\n")
        line_height = int(data.font_size * 1.4)  # Line spacing

        # Calculate starting Y position (center the block of text)
        total_height = line_height * len(lines)
        start_y = pos_y + total_height // 2

        for i, line in enumerate(lines):
            line_y = start_y - (i * line_height)
            position = OpenMaya.MPoint(pos_x, line_y, 0)

            draw_manager.text2d(
                position,
                line,
                OpenMayaRender.MUIDrawManager.kCenter,
                None,
                None,
                False,
            )

        draw_manager.endDrawable()


def initializePlugin(plugin):
    """Initialize the plugin."""
    plugin_fn = OpenMaya.MFnPlugin(plugin, "Maya Subtitler", "1.0", "Any")

    try:
        plugin_fn.registerNode(
            K_PLUGIN_NODE_NAME,
            K_PLUGIN_NODE_ID,
            SubtitleLocator.creator,
            SubtitleLocator.initialize,
            OpenMaya.MPxNode.kLocatorNode,
            K_PLUGIN_CLASSIFICATION,
        )
    except Exception as e:
        sys.stderr.write(f"Failed to register node: {e}\n")
        raise

    try:
        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator(
            K_PLUGIN_CLASSIFICATION,
            K_DRAW_REGISTRANT_ID,
            SubtitleLocatorDrawOverride.creator,
        )
    except Exception as e:
        sys.stderr.write(f"Failed to register draw override: {e}\n")
        raise


def uninitializePlugin(plugin):
    """Uninitialize the plugin."""
    plugin_fn = OpenMaya.MFnPlugin(plugin)

    try:
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator(
            K_PLUGIN_CLASSIFICATION, K_DRAW_REGISTRANT_ID
        )
    except Exception as e:
        sys.stderr.write(f"Failed to deregister draw override: {e}\n")
        raise

    try:
        plugin_fn.deregisterNode(K_PLUGIN_NODE_ID)
    except Exception as e:
        sys.stderr.write(f"Failed to deregister node: {e}\n")
        raise
