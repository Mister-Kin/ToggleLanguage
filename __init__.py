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

_modules=[
    "Function",
]

if "bpy" in locals():
    from importlib import reload
    _modules_loaded[:] = [reload(val) for val in _modules_loaded]
    del reload
else:
    import bpy
    for val in _modules:
        from . import(val)

__import__(name=__name__, fromlist=_modules)
_namespace = globals()
_modules_loaded = [_namespace[name] for name in _modules]
del _namespace

def register():
    from bpy.utils import register_class
    for mod in _modules_loaded:
        for cls in mod.ClassName:
            register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(Function.ButtonUI.draw)

def unregister():
    from bpy.utils import unregister_class
    for mod in _modules_loaded:
        for cls in mod.ClassName:
            unregister_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.remove(Function.ButtonUI.draw)
