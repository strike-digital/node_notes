from bpy.props import IntProperty
from bpy.types import AddonPreferences, Context, UILayout


class NNotesAddonPreferences(AddonPreferences):
    bl_idname = __package__.split(".")[0]
    layout: UILayout

    editor_width: IntProperty(
        name="Editor width",
        description="The default width to open the note editor with",
        default=500,
        subtype="PIXEL",
    )

    editor_height: IntProperty(
        name="Editor height",
        description="The default height to open the note editor with",
        default=500,
        subtype="PIXEL",
    )

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.prop(self, "editor_width")
        col.prop(self, "editor_height")


def get_prefs(context: Context) -> NNotesAddonPreferences:
    return context.preferences.addons[__package__.split(".")[0]].preferences
