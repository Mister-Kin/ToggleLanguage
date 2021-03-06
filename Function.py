import bpy
from bpy.types import Header, Menu, Panel, Operator

class ButtonUI(Header):
    bl_idname="ButtonUI"
    bl_space_type="TOPBAR"

    def draw(self, context):
        layout=self.layout

        lang = bpy.context.preferences.view.language
        row = layout.row(align=True)
        row.operator("function.toggle_language", text=lang_dict[lang]["toggle_button"])
        row.menu("Settings_Menu", text=lang_dict[lang]["settings_menu"])
        row.operator("screen.userpref_show",icon="PREFERENCES",text="")
        if lang!="en_US":
            if bpy.context.scene.new_data_translation==True:
                bpy.context.preferences.view.use_translate_new_dataname=True
            else:
                bpy.context.preferences.view.use_translate_new_dataname=False

class ToggleButtonFunction(Operator):
    bl_idname = "function.toggle_language"
    bl_label = "Toggle Button Function"
    bl_description = "Click Button to Toggle Language"

    def execute(self, context):
        lang=bpy.context.preferences.view.language
        if lang=="en_US":
            bpy.context.preferences.view.language="zh_CN"
        else:
            bpy.context.preferences.view.language="en_US"
        return {"FINISHED"}

class SettingsMenu(Menu):
    bl_idname="Settings_Menu"
    bl_label="Settings Menu"

    def draw(self, context):
        layout=self.layout

        lang=bpy.context.preferences.view.language
        if bpy.context.preferences.view.show_developer_ui==True:
            hint_scheme_type="hint_scheme_type_developer"
        else:
            hint_scheme_type="hint_scheme_type_default"
        col=layout.column(align=True)
        col.menu("Hint_Scheme", text=lang_dict[lang][hint_scheme_type])
        col.prop(context.scene, "new_data_translation", text=lang_dict[lang]["new_data_translation"])

    bpy.types.Scene.new_data_translation = bpy.props.BoolProperty(
    name = "New Data Translation",
    description = "Translation for New Data",
    default = False)

class HintScheme(Menu):
    bl_idname = "Hint_Scheme"
    bl_label= "Hint Scheme"

    def draw(self, context):
        layout = self.layout

        lang = bpy.context.preferences.view.language
        layout.operator("hint_scheme.default", text = lang_dict[lang]["hint_scheme_default"])
        layout.operator("hint_scheme.developer", text = lang_dict[lang]["hint_scheme_developer"])

class HintSchemeDeveloper(Operator):
    bl_idname = "hint_scheme.developer"
    bl_label = "Hint Scheme Developer"
    bl_description = "Hint Scheme for Developer"

    def execute(self, context):
        bpy.context.preferences.view.show_developer_ui=True
        bpy.context.preferences.view.show_tooltips_python=True
        return {"FINISHED"}

class HintSchemeDefault(Operator):
    bl_idname = "hint_scheme.default"
    bl_label = "Hint Scheme Default"
    bl_description = "Hint Scheme for Default"

    def execute(self, context):
        bpy.context.preferences.view.show_developer_ui=False
        bpy.context.preferences.view.show_tooltips_python=False
        return {"FINISHED"}

ClassName =(
    ButtonUI,
    ToggleButtonFunction,
    HintScheme,
    HintSchemeDeveloper,
    HintSchemeDefault,
    SettingsMenu,
)

lang_dict = { "zh_CN": { "toggle_button": "切换",
                         "settings_menu": "设置",
                         "hint_scheme": "提示方案",
                         "hint_scheme_type_default": "提示方案：默认",
                         "hint_scheme_type_developer": "提示方案：开发者",
                         "hint_scheme_default": "默认",
                         "hint_scheme_developer": "开发者",
                         "new_data_translation": "新建数据 - 翻译"},
              "en_US": { "toggle_button": "Toggle",
                         "settings_menu": "Settings",
                         "hint_scheme": "Hint Scheme",
                         "hint_scheme_type_default": "Hint Scheme: Default",
                         "hint_scheme_type_developer": "Hint Scheme: Developer",
                         "hint_scheme_default": "Default",
                         "hint_scheme_developer": "Developer",
                         "new_data_translation": "New Data - Translation"}
             }
