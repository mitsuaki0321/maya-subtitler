"""Maya Subtitler - Subtitle display tools for Maya."""

import importlib
import os

import maya.cmds as cmds

from . import command
from . import ui

importlib.reload(command)
importlib.reload(ui)

__version__ = "1.0.0"


def load_plugins():
    """Load all required plugins for maya_subtitler."""
    # Load the locator node plugin
    if not cmds.pluginInfo("subtitleLocator", query=True, loaded=True):
        cmds.loadPlugin("subtitleLocator")

    # Load the command plugin from this package
    if not cmds.pluginInfo("createSubtitleLocator", query=True, loaded=True):
        command_path = os.path.join(os.path.dirname(__file__), "command.py")
        cmds.loadPlugin(command_path)


def show_ui():
    """Show the subtitle locator UI."""
    load_plugins()
    ui.show()
