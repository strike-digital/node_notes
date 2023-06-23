import bpy
from bpy.types import UILayout
from ..operators.op_open_notes_editor import NNOTES_OT_open_notes_editor


def draw_node_notes_button(self, context):
    layout: UILayout = self.layout

    op = NNOTES_OT_open_notes_editor
    if op.poll(context):
        layout.operator(op.bl_idname, icon="TEXT")
    layout.separator()


def register():
    bpy.types.NODE_MT_context_menu.prepend(draw_node_notes_button)


def unregister():
    bpy.types.NODE_MT_context_menu.remove(draw_node_notes_button)