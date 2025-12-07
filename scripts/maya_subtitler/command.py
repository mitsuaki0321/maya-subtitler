"""
Maya command for creating subtitle locators.

Usage:
    import maya.cmds as cmds

    # Create with defaults
    cmds.createSubtitleLocator()

    # Create with options
    cmds.createSubtitleLocator(
        name="mySubtitle",
        subtitleFile="path/to/file.srt",
        fontSize=24,
        startFrame=101
    )
"""

from maya.api import OpenMaya


def maya_useNewAPI():
    pass


K_PLUGIN_CMD_NAME = "createSubtitleLocator"


class CreateSubtitleLocatorCmd(OpenMaya.MPxCommand):
    """Command to create a subtitle locator node."""

    # Flag definitions: (shortName, longName, argType)
    kNameFlag = "-n"
    kNameFlagLong = "-name"
    kFileFlag = "-f"
    kFileFlagLong = "-subtitleFile"
    kStartFrameFlag = "-sf"
    kStartFrameFlagLong = "-startFrame"
    kFontSizeFlag = "-fs"
    kFontSizeFlagLong = "-fontSize"
    kPositionXFlag = "-px"
    kPositionXFlagLong = "-positionX"
    kPositionYFlag = "-py"
    kPositionYFlagLong = "-positionY"
    kWrapTextFlag = "-wt"
    kWrapTextFlagLong = "-wrapText"
    kWordWrapFlag = "-ww"
    kWordWrapFlagLong = "-wordWrap"
    kMaxCharsFlag = "-mc"
    kMaxCharsFlagLong = "-maxCharsPerLine"
    kMaxLinesFlag = "-ml"
    kMaxLinesFlagLong = "-maxLines"

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)
        self._created_nodes = []

    @staticmethod
    def creator():
        return CreateSubtitleLocatorCmd()

    @staticmethod
    def createSyntax():
        syntax = OpenMaya.MSyntax()
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kNameFlag,
            CreateSubtitleLocatorCmd.kNameFlagLong,
            OpenMaya.MSyntax.kString,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kFileFlag,
            CreateSubtitleLocatorCmd.kFileFlagLong,
            OpenMaya.MSyntax.kString,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kStartFrameFlag,
            CreateSubtitleLocatorCmd.kStartFrameFlagLong,
            OpenMaya.MSyntax.kLong,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kFontSizeFlag,
            CreateSubtitleLocatorCmd.kFontSizeFlagLong,
            OpenMaya.MSyntax.kLong,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kPositionXFlag,
            CreateSubtitleLocatorCmd.kPositionXFlagLong,
            OpenMaya.MSyntax.kDouble,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kPositionYFlag,
            CreateSubtitleLocatorCmd.kPositionYFlagLong,
            OpenMaya.MSyntax.kDouble,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kWrapTextFlag,
            CreateSubtitleLocatorCmd.kWrapTextFlagLong,
            OpenMaya.MSyntax.kBoolean,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kWordWrapFlag,
            CreateSubtitleLocatorCmd.kWordWrapFlagLong,
            OpenMaya.MSyntax.kBoolean,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kMaxCharsFlag,
            CreateSubtitleLocatorCmd.kMaxCharsFlagLong,
            OpenMaya.MSyntax.kLong,
        )
        syntax.addFlag(
            CreateSubtitleLocatorCmd.kMaxLinesFlag,
            CreateSubtitleLocatorCmd.kMaxLinesFlagLong,
            OpenMaya.MSyntax.kLong,
        )
        return syntax

    def isUndoable(self):
        return True

    def doIt(self, args):
        # Parse arguments
        arg_parser = OpenMaya.MArgParser(self.syntax(), args)

        name = "subtitleLocator1"
        if arg_parser.isFlagSet(self.kNameFlag):
            name = arg_parser.flagArgumentString(self.kNameFlag, 0)

        subtitle_file = ""
        if arg_parser.isFlagSet(self.kFileFlag):
            subtitle_file = arg_parser.flagArgumentString(self.kFileFlag, 0)

        start_frame = 0
        if arg_parser.isFlagSet(self.kStartFrameFlag):
            start_frame = arg_parser.flagArgumentInt(self.kStartFrameFlag, 0)

        font_size = 18
        if arg_parser.isFlagSet(self.kFontSizeFlag):
            font_size = arg_parser.flagArgumentInt(self.kFontSizeFlag, 0)

        position_x = 0.0
        if arg_parser.isFlagSet(self.kPositionXFlag):
            position_x = arg_parser.flagArgumentDouble(self.kPositionXFlag, 0)

        position_y = -0.4
        if arg_parser.isFlagSet(self.kPositionYFlag):
            position_y = arg_parser.flagArgumentDouble(self.kPositionYFlag, 0)

        wrap_text = True
        if arg_parser.isFlagSet(self.kWrapTextFlag):
            wrap_text = arg_parser.flagArgumentBool(self.kWrapTextFlag, 0)

        word_wrap = True
        if arg_parser.isFlagSet(self.kWordWrapFlag):
            word_wrap = arg_parser.flagArgumentBool(self.kWordWrapFlag, 0)

        max_chars = 80
        if arg_parser.isFlagSet(self.kMaxCharsFlag):
            max_chars = arg_parser.flagArgumentInt(self.kMaxCharsFlag, 0)

        max_lines = 3
        if arg_parser.isFlagSet(self.kMaxLinesFlag):
            max_lines = arg_parser.flagArgumentInt(self.kMaxLinesFlag, 0)

        # Create nodes using MDagModifier for undo support
        self._dag_modifier = OpenMaya.MDagModifier()

        # Create transform node
        transform_obj = self._dag_modifier.createNode("transform")
        self._dag_modifier.renameNode(transform_obj, name)

        # Create locator shape
        shape_obj = self._dag_modifier.createNode("subtitleLocator", transform_obj)
        self._dag_modifier.renameNode(shape_obj, f"{name}Shape")

        self._dag_modifier.doIt()

        # Get the shape's MFnDependencyNode for setting attributes
        shape_fn = OpenMaya.MFnDependencyNode(shape_obj)

        # Set attributes
        if subtitle_file:
            plug = shape_fn.findPlug("subtitleFile", False)
            plug.setString(subtitle_file)

        plug = shape_fn.findPlug("startFrame", False)
        plug.setInt(start_frame)

        plug = shape_fn.findPlug("fontSize", False)
        plug.setInt(font_size)

        plug = shape_fn.findPlug("positionX", False)
        plug.setFloat(position_x)

        plug = shape_fn.findPlug("positionY", False)
        plug.setFloat(position_y)

        plug = shape_fn.findPlug("wrapText", False)
        plug.setBool(wrap_text)

        plug = shape_fn.findPlug("wordWrap", False)
        plug.setBool(word_wrap)

        plug = shape_fn.findPlug("maxCharsPerLine", False)
        plug.setInt(max_chars)

        plug = shape_fn.findPlug("maxLines", False)
        plug.setInt(max_lines)

        # Store for undo
        self._created_nodes = [transform_obj, shape_obj]

        # Get transform name and set as result
        transform_fn = OpenMaya.MFnDependencyNode(transform_obj)
        self.setResult(transform_fn.name())

    def redoIt(self):
        self._dag_modifier.doIt()

    def undoIt(self):
        self._dag_modifier.undoIt()


def initializePlugin(plugin):
    """Initialize the command plugin."""
    plugin_fn = OpenMaya.MFnPlugin(plugin, "Maya Subtitler", "1.0", "Any")
    try:
        plugin_fn.registerCommand(
            K_PLUGIN_CMD_NAME,
            CreateSubtitleLocatorCmd.creator,
            CreateSubtitleLocatorCmd.createSyntax,
        )
    except Exception as e:
        OpenMaya.MGlobal.displayError(f"Failed to register command: {e}")
        raise


def uninitializePlugin(plugin):
    """Uninitialize the command plugin."""
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(K_PLUGIN_CMD_NAME)
    except Exception as e:
        OpenMaya.MGlobal.displayError(f"Failed to deregister command: {e}")
        raise
