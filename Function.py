import bpy
from bpy.types import Header, Menu, Panel, Operator

class ButtonUI(Header):
    bl_idname="ButtonUI"
    bl_space_type="TOPBAR"

    def draw(self, context):
        layout=self.layout

        lang = bpy.context.preferences.view.language
        if lang=="en_US":
            toggle_button_text="Toggle"
        else:
            toggle_button_text="切换"

        if bpy.context.preferences.view.show_developer_ui==0:
            if lang=="en_US":
                Hint_Scheme_name="Default"
            else:
                Hint_Scheme_name="默认"
        else:
            if lang=="en_US":
                Hint_Scheme_name="Developer"
            else:
                Hint_Scheme_name="开发者"

        split = layout.split(factor=1)
        row = split.row(align=True)
        row.operator("function.toggle_language", text=toggle_button_text)
        row.menu("Hint_Scheme", text=Hint_Scheme_name)
        row.operator("screen.userpref_show",icon="PREFERENCES",text="")

class ToggleButtonFunction(Operator):
    bl_idname = "function.toggle_language"
    bl_label = "Toggle Button Function"
    bl_description = "Click Button to Toggle Language"

    def execute(self, context):
        lang=bpy.context.preferences.view.language
        if lang=="en_US":
            bpy.context.preferences.view.language="zh_CN"
            bpy.context.preferences.view.use_translate_new_dataname=False
        else:
            bpy.context.preferences.view.language="en_US"
        return {"FINISHED"}

class HintScheme(Menu):
    bl_idname = "Hint_Scheme"
    bl_label= "Hint_Scheme"

    def draw(self, context):
        layout = self.layout

        lang = bpy.context.preferences.view.language
        if lang=="en_US":
            hint_scheme_default_name="Default"
            hint_scheme_developer_name="Developer"
        else:
            hint_scheme_default_name="默认"
            hint_scheme_developer_name="开发者"

        layout.operator("hint_scheme.default", text = hint_scheme_default_name)
        layout.operator("hint_scheme.developer", text = hint_scheme_developer_name)

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
)
