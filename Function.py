import bpy
from bpy.types import Menu, Operator, PropertyGroup, AddonPreferences
from bpy.props import BoolProperty, EnumProperty
from bpy.app import translations
from multiprocessing import cpu_count


def Draw_UI(self, context):
    scene = context.scene
    userpref = context.preferences

    layout = self.layout
    row = layout.row(align=True)
    row.operator("function.toggle_language")
    row.menu("TOPBAR_MT_SettingsMenu")
    row.operator("screen.userpref_show", icon="PREFERENCES", text="")

    # 置于此处才能保证该复选框的绘制速度。
    if translations.locale != "en_US":
        if scene.my_properties.translate_new_data_name:
            userpref.view.use_translate_new_dataname = True
        else:
            userpref.view.use_translate_new_dataname = False


class TOPBAR_MT_SettingsMenu(Menu):
    bl_idname = "TOPBAR_MT_SettingsMenu"
    bl_label = "Settings"

    def draw(self, context):
        scene = context.scene
        userpref = context.preferences
        if userpref.view.show_developer_ui:
            hint_scheme_menu_name = "Current Hint Scheme: Developer"
        else:
            hint_scheme_menu_name = "Current Hint Scheme: Default"

        layout = self.layout
        col = layout.column(align=True)
        col.menu("TOPBAR_MT_HintScheme",
                 icon="TEXT",
                 text=hint_scheme_menu_name)
        col.prop(scene.my_properties, "translate_new_data_name")
        col.operator("function.load_my_settings", icon="SETTINGS")
        col.operator("function.load_factory_settings", icon="TOOL_SETTINGS")


class TOPBAR_MT_HintSchemeMenu(Menu):
    bl_idname = "TOPBAR_MT_HintScheme"
    bl_label = "Hint Scheme Menu"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("function.default_hint_scheme")
        col.operator("function.developer_hint_scheme")


def MessageBox(title="Message Box", message="", icon="INFO"):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw,
                                          title=translations.pgettext(title),
                                          icon=icon)


class ToggleButtonFunction(Operator):
    bl_idname = "function.toggle_language"
    bl_label = "Toggle"
    bl_description = "Click Button to Toggle Language"

    def execute(self, context):
        userpref = context.preferences
        addonpref = userpref.addons["ToggleLanguage"].preferences
        lang = translations.locale

        if addonpref.first_lang != addonpref.second_lang:
            if lang == addonpref.first_lang:
                userpref.view.language = addonpref.second_lang
            else:
                userpref.view.language = addonpref.first_lang
        else:
            MessageBox(
                title="Fail to Toggle Language",
                message=
                "Two Languages are Same! Please Select Two Different Languages for Addon.",
                icon="ERROR")
        return {"FINISHED"}


class DefaultHintSchemeFunction(Operator):
    bl_idname = "function.default_hint_scheme"
    bl_label = "Default Mode"
    bl_description = "Show No Extra Information"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = False
        userpref.view.show_tooltips_python = False
        self.report({"INFO"}, "Switch to Default Mode!")
        return {"FINISHED"}


class DeveloperHintSchemeFunction(Operator):
    bl_idname = "function.developer_hint_scheme"
    bl_label = "Developer Mode"
    bl_description = "Show Tooltips and Options for Developers"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = True
        userpref.view.show_tooltips_python = True
        self.report({"INFO"}, "Switch to Developer Mode!")
        return {"FINISHED"}


class LoadMySettingsFunction(Operator):
    bl_idname = "function.load_my_settings"
    bl_label = "Load My Settings"
    bl_description = "Load My Customized Settings of Startup File and Preferences"

    def execute(self, context):
        scene = context.scene
        userpref = context.preferences

        if userpref.version[1] >= 90:
            blender_v290 = True
        else:
            blender_v290 = False
        if userpref.version[0] == 3:
            blender_v3 = True
        else:
            blender_v3 = False

        # v2.93 及之后版本的文件命名有所变化
        if userpref.version[0] >= 3 or userpref.version[1] == 93:
            blender_light_theme_name = "Blender_Light.xml"
            blender_keyconfig_name = "Blender"
        else:
            blender_light_theme_name = "blender_light.xml"
            blender_keyconfig_name = "blender"

        userpref.view.ui_scale = 1.3
        if blender_v290 or blender_v3:
            userpref.view.show_statusbar_stats = True
            userpref.view.show_statusbar_memory = True
            if userpref.view.is_property_readonly("show_statusbar_vram"):
                pass  # 无显卡时，该属性为只读，无法对其进行写操作。
            else:
                userpref.view.show_statusbar_vram = True
        else:
            userpref.system.audio_device = "SDL"  # v2.83 及之前版本未引入系统原生的 API，用 SDL 替代。

        user_platform = bpy.app.build_platform
        execution_path = bpy.app.binary_path
        theme_path = "{First_Main_Number}.{Second_Main_Number}/scripts/presets/interface_theme/" + blender_light_theme_name
        theme_path = theme_path.format(First_Main_Number=userpref.version[0],
                                       Second_Main_Number=userpref.version[1])
        # b"Windows" b"Darwin" b"Linux"
        if user_platform == b"Windows":
            theme_path = execution_path.replace("blender.exe", theme_path)
        elif user_platform == b"Darwin":
            theme_path = execution_path.replace("MacOS/Blender",
                                                "Resources/" + theme_path)
        else:
            theme_path = execution_path[:-7] + theme_path
        bpy.ops.script.execute_preset(
            filepath=theme_path,
            menu_idname="USERPREF_MT_interface_theme_presets")

        bpy.ops.preferences.addon_enable(module="node_wrangler")
        bpy.ops.preferences.addon_enable(module="object_fracture_cell")
        bpy.ops.preferences.addon_enable(module="development_icon_get")
        # v3.0 及之后版本用的是 cyclesX，其中的 Auto Tiles 功能是为了减少内存占用，
        # 即渲染 tile 大小的图像数据并缓存进硬盘，渲染结束时再合并在一起。
        # 与老版的 cycles 渲染调度逻辑不一样，因此 auto_tile_size 插件在 v3.0 中被移除。
        if blender_v3:
            pass
        else:
            bpy.ops.preferences.addon_enable(module="render_auto_tile_size")

        userpref.inputs.use_rotate_around_active = True
        userpref.inputs.use_zoom_to_mouse = True

        kcpref = context.window_manager.keyconfigs[
            blender_keyconfig_name].preferences
        kcpref.use_pie_click_drag = True
        kcpref.use_v3d_shade_ex_pie = True

        userpref.filepaths.use_file_compression = True
        userpref.filepaths.use_auto_save_temporary_files = False
        userpref.filepaths.texture_directory = "H:/Textures/"
        userpref.filepaths.temporary_directory = "E:/Temp/"
        userpref.filepaths.render_cache_directory = "E:/Temp/"
        userpref.filepaths.render_output_directory = "E:/Process/"
        scene.render.filepath = "E:/Process/"

        scene.render.engine = "CYCLES"
        cpref = userpref.addons["cycles"].preferences
        cpref.get_devices()  # 刷新设备
        # 获取当前版本支持的设备类型，逐一设置以检测是否存在显卡。
        for device_type in cpref.get_device_types(bpy.context):
            try:
                cpref.compute_device_type = device_type[0]
                if cpref.has_active_device():
                    gpu_exist = True
                    break
                else:
                    gpu_exist = False
                    cpref.compute_device_type = "NONE"
            except TypeError:
                pass
        if gpu_exist:
            cpref.get_devices()
            for device in cpref.devices:
                device.use = True
            scene.cycles.device = "GPU"
        else:
            pass
        if blender_v3:
            pass
        else:
            scene.cycles.use_adaptive_sampling = True
            scene.cycles.adaptive_threshold = 0.1
            scene.ats_settings.cpu_choice = "256"
        scene.render.threads_mode = "FIXED"
        scene.render.threads = max(1, cpu_count() - 2)
        bpy.ops.wm.save_userpref()
        bpy.ops.wm.save_homefile()
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class LoadFactorySettingsFunction(Operator):
    bl_idname = "function.load_factory_settings"
    bl_label = "Load Factory Settings"
    bl_description = "Load Factory Settings of Startup File and Preferences"

    def execute(self, context):
        bpy.ops.wm.read_factory_settings()
        bpy.ops.wm.save_userpref()
        bpy.ops.wm.save_homefile()
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class MyProperties(PropertyGroup):
    """
    # 使用即时绘制 UI 的方式，弃用 property 的 update 函数，即 bpy.props 中 property 值更改之时会调用的函数。该方式没法直接接管用户偏好设置，用户仍可在偏好设置中设置 translate_new_dataname 选项，可能导致出现与本插件的 BoolProperty 值不符的情况。
    def set_translate_new_data_name_state(self, context):
        scene = context.scene
        userpref = context.preferences
        lang = userpref.view.language
        if lang != "en_US":
            if scene.my_properties.translate_new_data_name:
                userpref.view.use_translate_new_dataname = True
            else:
                userpref.view.use_translate_new_dataname = False
        return {"FINISHED"}
    """

    translate_new_data_name: BoolProperty(
        name="Translate New Data-Block's Name",
        description="Enable or Disable Translation of New Data-Block's Name",
        default=False)


class AddonPref(AddonPreferences):
    bl_idname = __package__

    # 在 AddonPreferences class 之下，property 值才能随着用户偏好设置自动保存。
    first_lang: EnumProperty(items=[
        ("zh_CN", "Simplified Chinese (简体中文)", "zh_CN", 1),
        ("zh_TW", "Traditional Chinese (繁體中文)", "zh_TW", 2),
        ("en_US", "English (English)", "en_US", 3),
        ("es", "Spanish (Español)", "es", 4),
        ("ja_JP", "Japanese (日本語)", "ja_JP", 5),
        ("sk_SK", "Slovak (Slovenčina)", "sk_SK", 6),
        ("uk_UA", "Ukrainian (Український)", "uk_UA", 7),
        ("vi_VN", "Vietnamese (tiếng Việt)", "vi_VN", 8),
        ("ar_EG", "Arabic (ﺔﻴﺑﺮﻌﻟﺍ)", "ar_EG", 9),
        ("cs_CZ", "Czech (Český)", "cs_CZ", 10),
        ("de_DE", "German (Deutsch)", "de_DE", 11),
        ("fr_FR", "French (Français)", "fr_FR", 12),
        ("it_IT", "Italian (Italiano)", "it_IT", 13),
        ("ko_KR", "Korean (한국 언어)", "ko_KR", 14),
        ("pt_BR", "Brazilian Portuguese (Português do Brasil)", "pt_BR", 15),
        ("pt_PT", "Portuguese (Português)", "pt_PT", 16),
        ("ru_RU", "Russian (Русский)", "ru_RU", 17)
    ],
                             name="First Language",
                             description="First Language for Toggling",
                             default="zh_CN")

    second_lang: EnumProperty(items=[
        ("zh_CN", "Simplified Chinese (简体中文)", "zh_CN", 1),
        ("zh_TW", "Traditional Chinese (繁體中文)", "zh_TW", 2),
        ("en_US", "English (English)", "en_US", 3),
        ("es", "Spanish (Español)", "es", 4),
        ("ja_JP", "Japanese (日本語)", "ja_JP", 5),
        ("sk_SK", "Slovak (Slovenčina)", "sk_SK", 6),
        ("uk_UA", "Ukrainian (Український)", "uk_UA", 7),
        ("vi_VN", "Vietnamese (tiếng Việt)", "vi_VN", 8),
        ("ar_EG", "Arabic (ﺔﻴﺑﺮﻌﻟﺍ)", "ar_EG", 9),
        ("cs_CZ", "Czech (Český)", "cs_CZ", 10),
        ("de_DE", "German (Deutsch)", "de_DE", 11),
        ("fr_FR", "French (Français)", "fr_FR", 12),
        ("it_IT", "Italian (Italiano)", "it_IT", 13),
        ("ko_KR", "Korean (한국 언어)", "ko_KR", 14),
        ("pt_BR", "Brazilian Portuguese (Português do Brasil)", "pt_BR", 15),
        ("pt_PT", "Portuguese (Português)", "pt_PT", 16),
        ("ru_RU", "Russian (Русский)", "ru_RU", 17)
    ],
                              name="Second Language",
                              description="Second Language for Toggling",
                              default="en_US")

    def draw(self, context):
        layout = self.layout
        layout.label(
            text="Please Select Two Languages for Addon to Toggle UI Language."
        )
        row = layout.row(align=True)
        row.prop(self, "first_lang")
        row.separator()
        row.prop(self, "second_lang")


ClassName = (
    TOPBAR_MT_SettingsMenu,
    TOPBAR_MT_HintSchemeMenu,
    ToggleButtonFunction,
    DefaultHintSchemeFunction,
    DeveloperHintSchemeFunction,
    LoadMySettingsFunction,
    LoadFactorySettingsFunction,
    MyProperties,
    AddonPref,
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
