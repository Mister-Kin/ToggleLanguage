# Copyright (C) Mr. Kin - Toggle Language
# License: http://www.gnu.org/licenses/gpl.html GPL version 3 or higher

# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name" : "Toggle Language",
    "author" : "Mr. Kin",
    "description" : "One Click to Toggle UI between Two Language",
    "blender" : (2, 83, 0),
    "version" : (0, 5),
    "location" : "Topbar",
    "warning" : "",
    "category" : "Interface",
    "doc_url": "https://mister-kin.github.io/ToggleLanguage/",
    "tracker_url": "https://mister-kin.github.io/about/#联系方式",
}

import bpy
from bpy.types import Header, Menu, Panel, Operator
from bpy.utils import register_class, unregister_class

class ButtonUI(Header):
    bl_idname="ButtonUI"
    bl_space_type="TOPBAR"

    def draw(self, context):
        region = context.region

        if region.alignment == "RIGHT":
            self.draw_right(context)
        else:
            pass

    def draw_right(self, context):
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
        row.operator("toggle_button.function", text=toggle_button_text)
        row.menu("Hint_Scheme", text=Hint_Scheme_name)
        row.operator("screen.userpref_show",icon="PREFERENCES",text="")

class ToggleButtonFunction(Operator):
    bl_idname = "toggle_button.function"
    bl_label = "Toggle Button Function"
    bl_description = "Click Button to Toggle Language"

    def execute(self, context):
        lang=bpy.context.preferences.view.language
        if lang=="en_US":
            bpy.context.preferences.view.language="zh_CN"
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
        bpy.context.preferences.view.show_developer_ui=1
        bpy.context.preferences.view.show_tooltips_python=1
        return {"FINISHED"}

class HintSchemeDefault(Operator):
    bl_idname = "hint_scheme.default"
    bl_label = "Hint Scheme Default"
    bl_description = "Hint Scheme for Default"

    def execute(self, context):
        bpy.context.preferences.view.show_developer_ui=0
        bpy.context.preferences.view.show_tooltips_python=0
        return {"FINISHED"}

classes ={
    ButtonUI,
    ToggleButtonFunction,
    HintScheme,
    HintSchemeDeveloper,
    HintSchemeDefault,
}

def register():
    for x in classes:
        register_class(x)

def unregister():
    for x in classes:
        unregister_class(x)

# only for live edit.
if __name__=="__main__":
    register()
