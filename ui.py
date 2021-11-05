import bpy
from bpy.types import Menu
from bpy.app import translations


def draw_ui(self, context):
    scene = context.scene
    userpref = context.preferences

    layout = self.layout
    row = layout.row(align=True)
    row.operator("toggle_language.toggle_language")
    row.menu("TOGGLE_LANGUAGE_MT_settings")
    row.operator("screen.userpref_show", icon="PREFERENCES", text="")

    # 置于此处才能保证 translate_new_dataname 复选框的更新速度。
    # 而如果放在 TOGGLE_LANGUAGE_MT_settings 类中，会慢很多。
    # 也不采用 property 的 update 函数，因为无法接管用户偏好设置。
    if translations.locale != "en_US":
        if scene.toggle_language_settings.translate_new_dataname:
            userpref.view.use_translate_new_dataname = True
        else:
            userpref.view.use_translate_new_dataname = False


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
        col.menu("TOGGLE_LANGUAGE_MT_hint_scheme",
                 icon="TEXT",
                 text=hint_scheme_menu_name)
        col.prop(scene.toggle_language_settings, "translate_new_dataname")
        col.operator("toggle_language.load_my_settings", icon="SETTINGS")
        col.operator("toggle_language.load_factory_settings",
                     icon="TOOL_SETTINGS")


class TOGGLE_LANGUAGE_MT_hint_scheme(Menu):
    bl_idname = "TOGGLE_LANGUAGE_MT_hint_scheme"
    bl_label = "Hint Scheme Menu"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("toggle_language.use_default_hint_scheme")
        col.operator("toggle_language.use_developer_hint_scheme")


classes = (
    TOGGLE_LANGUAGE_MT_settings,
    TOGGLE_LANGUAGE_MT_hint_scheme,
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
