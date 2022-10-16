import bpy

addon_keymaps = []


def register_keymaps():
    wm = bpy.context.window_manager

    km = wm.keyconfigs.addon.keymaps.new(name="Window")
    kmi = km.keymap_items.new(idname="toggle_language.toggle_language",
                              type="F5",
                              value="PRESS")
    addon_keymaps.append((km, kmi))

    km = wm.keyconfigs.addon.keymaps.new(name="Window")
    kmi = km.keymap_items.new(idname="screen.userpref_show",
                              type="U",
                              value="PRESS",
                              ctrl=True,
                              alt=True)
    addon_keymaps.append((km, kmi))


def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def register():
    register_keymaps()


def unregister():
    unregister_keymaps()
