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

bl_info = {
    "name" : "Switch Language",
    "author" : "Mr. Kin",
    "description" : "One Click To Switch Language Between ZH and EN",
    "blender" : (2, 80, 0),
    "version" : (0, 2),
    "location" : "Topbar & Info Line",
    "warning" : "",
    "category" : "Interface",
    "wiki_url": "https://mister-kin.github.io/",
    "tracker_url": "https://mister-kin.github.io/about/#联系方式",
}

import bpy
from bpy.types import Header, Menu, Panel, Operator

class SwitchLanguage(Header):
    bl_idname='SwitchLanguage'
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
        layout.operator('click.switch', text=button_text)

class ClickSwitch(Operator):
    bl_idname = 'click.switch'
    bl_label = 'Click 2 Switch'
    bl_description = 'Click Button to Switch Language'

    def execute(self, context):
        l=bpy.context.preferences.view.language
        if l=='en_US':
            bpy.context.preferences.view.language='zh_CN'
        else:
            bpy.context.preferences.view.language='en_US'
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SwitchLanguage)
    bpy.utils.register_class(ClickSwitch)

def unregister():
    bpy.utils.unregister_class(SwitchLanguage)
    bpy.utils.unregister_class(ClickSwitch)

if __name__=='__main__':
    register()
