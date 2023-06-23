import bpy
import blf
from bpy.types import Context, Operator, Window
from mathutils import Vector as V
from ..helpers.view import dpifac
from ..helpers.btypes import BOperator


def close_window(window: Window):
    area = window.screen.areas[0]
    area.type = "IMAGE_EDITOR"
    bpy.ops.render.view_cancel("INVOKE_DEFAULT")


@BOperator("nnotes", undo=True)
class NNOTES_OT_close_notes_editor(Operator):

    @classmethod
    def poll(cls, context):
        for window in context.window_manager.windows:
            space = window.screen.areas[0].spaces.active
            if hasattr(space, "text") and space.text:
                return True
        else:
            return False

    def execute(self, context: Context):
        for window in context.window_manager.windows:
            space = window.screen.areas[0].spaces.active
            if hasattr(space, "text") and space.text:
                text = space.text
                close_window(window)

        frames = []
        areas = []
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == "NODE_EDITOR":
                    if node_tree := area.spaces.active.node_tree:
                        for node in node_tree.nodes:
                            if node.type == "FRAME" and node.text == text:
                                areas.append(area)
                                frames.append(node)

        # All of this is a guess and isn't very reliable.
        # It tries to calculate the correct width and height to fit all of the text in the frame.
        for frame, area in zip(frames, areas):
            text = "".join([l.body for l in frame.text.lines])
            dims = V((0, 0))
            blf.size(0, frame.label_size, 72)
            for line in frame.text.lines:
                body = line.body
                if not body:
                    body = "I"
                dims[0] = max(dims[0], blf.dimensions(0, body)[0])
                dims[1] = dims[1] + blf.dimensions(0, body)[1] + frame.label_size / 3

            dims *= dpifac()
            frame.width = dims[0] if frame.width < dims[0] else frame.width
            frame.height = dims[1] if frame.height < dims[1] else frame.height

        return {"FINISHED"}