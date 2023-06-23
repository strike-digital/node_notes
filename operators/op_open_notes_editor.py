import bpy
from bpy.types import Operator, Window
from ..prefs import get_prefs
from ..helpers.btypes import BOperator


def call_new_window(window_type: str, width: int, height: int):
    """
    Taken from https://github.com/schroef/Custom-Preferences-Size, this is so useful.
    """

    # Modify scene settings
    render = bpy.context.scene.render
    prefs = bpy.context.preferences
    view = prefs.view
    orgResX = render.resolution_x
    orgResY = render.resolution_y
    render.resolution_x = int(width)
    render.resolution_y = int(height)
    orgDispMode = view.render_display_type
    view.render_display_type = "WINDOW"

    # Call image editor window
    bpy.ops.render.view_show("INVOKE_DEFAULT")

    # Change area type
    area = bpy.context.window_manager.windows[-1].screen.areas[0]
    area.type = window_type

    # Restore old values
    view.render_display_type = orgDispMode
    render.resolution_x = orgResX
    render.resolution_y = orgResY

    return bpy.context.window_manager.windows[-1]


def highlight_window(window: Window):
    area = window.screen.areas[0]
    area_type = area.type
    area.type = "IMAGE_EDITOR"
    bpy.ops.render.view_show("INVOKE_DEFAULT")
    area.type = area_type


@BOperator("nnotes")
class NNOTES_OT_open_notes_editor(Operator):

    @classmethod
    def poll(cls, context):
        if context.area.type != "NODE_EDITOR":
            return False
        return context.active_node and context.active_node.type == "FRAME"

    def execute(self, context):
        node = context.active_node
        if node.type == "FRAME":
            if not node.text:
                node.text = bpy.data.texts.new(node.name + "_note")
            text = node.text

            for window in context.window_manager.windows:
                space = window.screen.areas[0].spaces.active
                if hasattr(space, "text") and space.text == text:
                    highlight_window(window)
                    break
            else:
                prefs = get_prefs(context)
                window = call_new_window("TEXT_EDITOR", prefs.editor_width, prefs.editor_height)

            area = window.screen.areas[0]
            space = area.spaces.active
            space.text = text
            space.show_syntax_highlight = False
            space.show_word_wrap = True
            space.show_region_header = False
            space.show_region_footer = False

            with context.temp_override(window=window, area=area):
                bpy.ops.text.move(type='FILE_TOP')

        return {"FINISHED"}