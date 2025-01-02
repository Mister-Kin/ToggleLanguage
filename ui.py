import bpy
from bpy.types import Menu
from bpy.app import translations


def draw_ui(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator("toggle_language.toggle_language")
    row.menu("TOGGLE_LANGUAGE_MT_utilities")
    row.menu("TOGGLE_LANGUAGE_MT_settings")
    row.operator("screen.userpref_show", icon="PREFERENCES", text="")


class TOGGLE_LANGUAGE_MT_settings(Menu):
    bl_idname = "TOGGLE_LANGUAGE_MT_settings"
    bl_label = "Settings"

    def draw(self, context):
        scene = context.scene
        userpref = context.preferences
        if userpref.view.show_developer_ui:
            hint_scheme_menu_name = "Current Hint Scheme: Developer"
        else:
            hint_scheme_menu_name = "Current Hint Scheme: Default"

        layout = self.layout
        col = layout.column(align=True)
        col.menu(
            "TOGGLE_LANGUAGE_MT_hint_scheme", icon="TEXT", text=hint_scheme_menu_name
        )
        col.prop(scene.toggle_language_settings, "translate_new_dataname")
        col.operator("toggle_language.load_my_blender_settings", icon="SETTINGS")
        col.operator(
            "toggle_language.load_blender_factory_settings", icon="TOOL_SETTINGS"
        )


class TOGGLE_LANGUAGE_MT_hint_scheme(Menu):
    bl_idname = "TOGGLE_LANGUAGE_MT_hint_scheme"
    bl_label = "Hint Scheme Menu"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("toggle_language.use_default_hint_scheme")
        col.operator("toggle_language.use_developer_hint_scheme")


class TOGGLE_LANGUAGE_MT_utilities(Menu):
    bl_idname = "TOGGLE_LANGUAGE_MT_utilities"
    bl_label = "Utilities"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(
            "toggle_language.delete_all_collections_and_objects",
            icon="OUTLINER_COLLECTION",
        )
        col.operator("toggle_language.add_video_progress_bar", icon="TOPBAR")
        col.operator("toggle_language.import_blueprint", icon="IMAGE_REFERENCE")


classes = (
    TOGGLE_LANGUAGE_MT_settings,
    TOGGLE_LANGUAGE_MT_hint_scheme,
    TOGGLE_LANGUAGE_MT_utilities,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(draw_ui)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.remove(draw_ui)
