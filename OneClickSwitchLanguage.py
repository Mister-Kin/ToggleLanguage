# Copyright (C) Mr. Kin - One Click Switch Language
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
    "name" : "One Click Switch Language",
    "author" : "Mr. Kin",
    "description" : "One Click to Switch UI between Two Language",
    "blender" : (2, 80, 0),
    "version" : (0, 3),
    "location" : "Topbar & Info Line",
    "warning" : "",
    "category" : "Interface",
    "doc_url": "https://mister-kin.github.io/OneClickSwitchLanguage/",
    "tracker_url": "https://mister-kin.github.io/about/#联系方式",
}

import bpy
from bpy.types import Header, Menu, Panel, Operator

class SwitchButtonUI(Header):
    bl_idname='SwitchButtonUI'
    bl_space_type='TOPBAR'

    def draw(self, context):
        region = context.region

        if region.alignment == 'RIGHT':
            pass
        else:
            self.draw_left(context)

    def draw_left(self,context):
        layout=self.layout
        l = bpy.context.preferences.view.language
        if l=='en_US':
            button_text='Switch Chinese'
        else:
            button_text='切换英语'
        layout.operator('button.function', text=button_text)

class ButtonFunction(Operator):
    bl_idname = 'button.function'
    bl_label = 'Button Function'
    bl_description = 'Click Button to Switch Language'

    def execute(self, context):
        l=bpy.context.preferences.view.language
        if l=='en_US':
            bpy.context.preferences.view.language='zh_CN'
        else:
            bpy.context.preferences.view.language='en_US'
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SwitchButtonUI)
    bpy.utils.register_class(ButtonFunction)

def unregister():
    bpy.utils.unregister_class(SwitchButtonUI)
    bpy.utils.unregister_class(ButtonFunction)

if __name__=='__main__':
    register()
