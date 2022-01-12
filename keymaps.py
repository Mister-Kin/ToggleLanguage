import bpy

addon_keymaps = []


def register_keymaps():
    wm = bpy.context.window_manager

    km = wm.keyconfigs.addon.keymaps.new(name="Window")
    kmi = km.keymap_items.new(idname="toggle_language.toggle_language",
                              type="F5",
                              value="PRESS")
    addon_keymaps.append((km, kmi))

    # 没有第三方软件全局占用 F3 键的情况了，故注释掉该功能
    """
    km = wm.keyconfigs.addon.keymaps.new(name="Window")
    kmi = km.keymap_items.new(idname="wm.search_menu",
                              type="F6",
                              value="PRESS")
    addon_keymaps.append((km, kmi))
    """

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
