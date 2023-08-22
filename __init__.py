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
    "name": "Toggle Language",
    "description": "One click to toggle UI between two languages",
    "author": "Mr. Kin",
    "version": (1, 5, 1),
    "blender": (2, 83, 0),
    "location": "Topbar Menu",
    "category": "Interface",
    "doc_url":
    "https://mister-kin.github.io/works/software-works/toggle-language/",
    "tracker_url": "https://mister-kin.github.io/about/#联系方式",
}

_modules = [
    "keymaps",
    "operators",
    "properties",
    "ui",
    "languages",
]

# support reloading sub-modules (refer to scripts/startup/bl_ui/__init__.py)
if "bpy" in locals():
    from importlib import reload
    _modules_loaded[:] = [reload(val) for val in _modules_loaded]
    del reload

__import__(name=__name__, fromlist=_modules)
_namespace = locals()
_modules_loaded = [_namespace[name] for name in _modules]
del _namespace


def register():
    for mod in _modules_loaded:
        mod.register()


def unregister():
    for mod in _modules_loaded:
        mod.unregister()
