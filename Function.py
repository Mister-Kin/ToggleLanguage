import bpy
from bpy.types import Header, Menu, Operator


class TOPBAR_HT_ButtonUI(Header):
    bl_idname = "TOPBAR_HT_ButtonUI"
    bl_space_type = "TOPBAR"

    def draw(self, context):
        scene = context.scene
        userpref = context.preferences
        lang = userpref.view.language

        layout = self.layout
        row = layout.row(align=True)
        row.operator("function.toggle_language",
                     text=lang_dict[lang]["toggle_button"])
        row.menu("TOPBAR_MT_SettingsMenu",
                 text=lang_dict[lang]["settings_menu"])
        row.operator("screen.userpref_show", icon="PREFERENCES", text="")
        if lang != "en_US":
            if scene.new_data_translation == True:
                userpref.view.use_translate_new_dataname = True
            else:
                userpref.view.use_translate_new_dataname = False


class ToggleButtonFunction(Operator):
    bl_idname = "function.toggle_language"
    bl_label = "Toggle Button Function"
    bl_description = "Click Button to Toggle Language"

    def execute(self, context):
        userpref = context.preferences
        lang = userpref.view.language

        if lang == "en_US":
            userpref.view.language = "zh_CN"
        else:
            userpref.view.language = "en_US"
        return {"FINISHED"}


class TOPBAR_MT_SettingsMenu(Menu):
    bl_idname = "TOPBAR_MT_SettingsMenu"
    bl_label = "Settings Menu"

    def draw(self, context):
        scene = context.scene
        userpref = context.preferences
        lang = userpref.view.language
        if userpref.view.show_developer_ui == True:
            hint_scheme_type = "hint_scheme_type_developer"
        else:
            hint_scheme_type = "hint_scheme_type_default"

        layout = self.layout
        col = layout.column(align=True)
        col.menu("TOPBAR_MT_HintScheme",
                 icon="TEXT",
                 text=lang_dict[lang][hint_scheme_type])
        col.prop(scene,
                 "new_data_translation",
                 text=lang_dict[lang]["new_data_translation"])
        col.operator("my.preferences",
                     icon="SETTINGS",
                     text=lang_dict[lang]["my_preferences"])
        col.operator("reset.preferences",
                     icon="TOOL_SETTINGS",
                     text=lang_dict[lang]["reset_preferences"])

    bpy.types.Scene.new_data_translation = bpy.props.BoolProperty(
        name="New Data Translation",
        description="Translation for New Data",
        default=False)


class TOPBAR_MT_HintScheme(Menu):
    bl_idname = "TOPBAR_MT_HintScheme"
    bl_label = "Hint Scheme"

    def draw(self, context):
        lang = context.preferences.view.language

        layout = self.layout
        col = layout.column(align=True)
        col.operator("hint_scheme.default",
                     text=lang_dict[lang]["hint_scheme_default"])
        col.operator("hint_scheme.developer",
                     text=lang_dict[lang]["hint_scheme_developer"])


class HintSchemeDeveloper(Operator):
    bl_idname = "hint_scheme.developer"
    bl_label = "Hint Scheme Developer"
    bl_description = "Hint Scheme for Developer"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = True
        userpref.view.show_tooltips_python = True
        return {"FINISHED"}


class HintSchemeDefault(Operator):
    bl_idname = "hint_scheme.default"
    bl_label = "Hint Scheme Default"
    bl_description = "Hint Scheme for Default"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = False
        userpref.view.show_tooltips_python = False
        return {"FINISHED"}


class MyPreferences(Operator):
    bl_idname = "my.preferences"
    bl_label = "My Preferences"
    bl_description = "My Customized Preferences"

    def execute(self, context):
        scene = context.scene
        userpref = context.preferences

        userpref.view.ui_scale = 1.3

        theme_path = "C:\\Program Files\\Blender Foundation\\Blender {First_Main_Number}.{Second_Main_Number}\\{First_Main_Number}.{Second_Main_Number}\\scripts\\presets\\interface_theme\\blender_light.xml"
        theme_path = theme_path.format(First_Main_Number=userpref.version[0],
                                       Second_Main_Number=userpref.version[1])
        bpy.ops.script.execute_preset(
            filepath=theme_path,
            menu_idname="USERPREF_MT_interface_theme_presets")

        bpy.ops.preferences.addon_enable(module="node_wrangler")
        bpy.ops.preferences.addon_enable(module="object_fracture_cell")
        bpy.ops.preferences.addon_enable(module="render_auto_tile_size")
        bpy.ops.preferences.addon_enable(module="development_icon_get")
        userpref.inputs.use_rotate_around_active = True
        userpref.inputs.use_zoom_to_mouse = True
        context.window_manager.keyconfigs['blender'].preferences[
            'use_pie_click_drag'] = True  # 设置后需重启 blender，否则无法正常使用该功能（除非手动设置）
        context.window_manager.keyconfigs['blender'].preferences[
            'use_v3d_shade_ex_pie'] = True

        userpref.addons['cycles'].preferences.compute_device_type = "CUDA"
        #userpref.addons['cycles'].preferences.devices[0].use = True # 一般显卡会自动启用。
        #userpref.addons['cycles'].preferences.devices[1].use = True # CUDA启用问题，目前 CYCLES 的 GPU 选项依然会是灰色，且手动点击查看才能解决。同时，直接开启该选项，插件目前会检测不出 CUDA 设备，导致「超出数据下标范围」的错误。
        userpref.system.audio_device = "SDL"

        userpref.filepaths.use_file_compression = True
        userpref.filepaths.use_auto_save_temporary_files = False
        userpref.filepaths.texture_directory = "H:\\Textures\\"
        userpref.filepaths.temporary_directory = "E:\\Temp\\"
        userpref.filepaths.render_cache_directory = "E:\\Temp\\"
        userpref.filepaths.render_output_directory = "E:\\Process\\"

        scene.render.filepath = "E:\\Process\\"
        scene.render.engine = "CYCLES"
        scene.cycles.device = "GPU"
        scene.cycles.use_adaptive_sampling = True
        scene.ats_settings.cpu_choice = "256"
        scene.render.threads_mode = "FIXED"
        scene.render.threads = 6
        bpy.ops.wm.save_homefile()

        userpref.view.show_statusbar_stats = True
        userpref.view.show_statusbar_memory = True
        userpref.view.show_statusbar_vram = True
        return {"FINISHED"}


class ResetPreferences(Operator):
    bl_idname = "reset.preferences"
    bl_label = "Reset Preferences"
    bl_description = "Reset Preferences"

    def execute(self, context):
        bpy.ops.wm.read_factory_userpref()
        bpy.ops.wm.save_userpref()
        #bpy.ops.wm.read_factory_settings() # Load Factory Startup File Settings 会导致闪退，故不考虑加入该功能
        #bpy.ops.wm.save_homefile()
        return {"FINISHED"}


ClassName = (
    TOPBAR_HT_ButtonUI,
    ToggleButtonFunction,
    TOPBAR_MT_HintScheme,
    HintSchemeDefault,
    HintSchemeDeveloper,
    TOPBAR_MT_SettingsMenu,
    MyPreferences,
    ResetPreferences,
)

addon_keymaps = []


def register_keymaps():
    wm = bpy.context.window_manager

    km = wm.keyconfigs.addon.keymaps.new(name="Window")
    kmi = km.keymap_items.new(idname="function.toggle_language",
                              type="F5",
                              value="PRESS")
    addon_keymaps.append((km, kmi))

    km = wm.keyconfigs.addon.keymaps.new(name="Window")
    kmi = km.keymap_items.new(idname="wm.search_menu",
                              type="F6",
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


lang_dict = {
    "zh_CN": {
        "toggle_button": "切换",
        "settings_menu": "设置",
        "hint_scheme": "提示方案",
        "hint_scheme_type_default": "提示方案：默认",
        "hint_scheme_type_developer": "提示方案：开发者",
        "hint_scheme_default": "默认模式",
        "hint_scheme_developer": "开发者模式",
        "new_data_translation": "新建数据 - 翻译",
        "my_preferences": "我的偏好设置",
        "reset_preferences": "重置偏好设置"
    },
    "en_US": {
        "toggle_button": "Toggle",
        "settings_menu": "Settings",
        "hint_scheme": "Hint Scheme",
        "hint_scheme_type_default": "Hint Scheme: Default",
        "hint_scheme_type_developer": "Hint Scheme: Developer",
        "hint_scheme_default": "Default Mode",
        "hint_scheme_developer": "Developer Mode",
        "new_data_translation": "New Data - Translation",
        "my_preferences": "My Preferences",
        "reset_preferences": "Reset Preferences"
    }
}
