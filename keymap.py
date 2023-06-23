import bpy
from .operators.op_close_notes_editor import NNOTES_OT_close_notes_editor
from .operators.op_open_notes_editor import NNOTES_OT_open_notes_editor

POSSIBLE_VALUES = ["type", "value", "shift", "ctrl", "alt", "oskey", "any", "key_modifier", "direction", "repeat"]

addon_keymaps: list[tuple[bpy.types.KeyMap, bpy.types.KeyMapItem]] = []


def get_user_kmi_from_addon_kmi(km_name, kmi_idname, prop_name):
    '''
    returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
    if there are multiple hotkeys!),
    That can actually be edited by the user (not possible with) the addon keymap
    '''
    user_keymap = bpy.context.window_manager.keyconfigs.user.keymaps[km_name]
    kmi_names = user_keymap.keymap_items.keys()
    for i, km_item in enumerate(user_keymap.keymap_items):
        if kmi_names[i] == kmi_idname:
            if user_keymap.keymap_items[i].properties.name == prop_name:
                return km_item
    return None  # not needed, since no return means None, but keeping for readability


def register():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window')
        kmi = km.keymap_items.new(
            idname=NNOTES_OT_open_notes_editor.bl_idname,
            type="LEFTMOUSE",
            value="DOUBLE_CLICK",
        )
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            idname=NNOTES_OT_close_notes_editor.bl_idname,
            type="ESC",
            value="PRESS",
        )
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            idname=NNOTES_OT_close_notes_editor.bl_idname,
            type="RET",
            value="PRESS",
            ctrl=True,
        )
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()