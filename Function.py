import bpy
from bpy.types import Header, Menu, Operator


class ButtonUI(Header):
    bl_idname = "ButtonUI"
    bl_space_type = "TOPBAR"

    def draw(self, context):
        scene = context.scene
        userpref = context.preferences
        lang = userpref.view.language

        layout = self.layout
        row = layout.row(align=True)
        row.operator("function.toggle_language", text=lang_dict[lang]["toggle_button"])
        row.menu("Settings_Menu", text=lang_dict[lang]["settings_menu"])
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


class SettingsMenu(Menu):
    bl_idname = "Settings_Menu"
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
        col.menu("Hint_Scheme", text=lang_dict[lang][hint_scheme_type])
        col.prop(scene,
                 "new_data_translation",
                 text=lang_dict[lang]["new_data_translation"])
        col.operator("my.preferences",
                     icon="PREFERENCES",
                     text=lang_dict[lang]["my_preferences"])

    bpy.types.Scene.new_data_translation = bpy.props.BoolProperty(
        name="New Data Translation",
        description="Translation for New Data",
        default=False)


class HintScheme(Menu):
    bl_idname = "Hint_Scheme"
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
        bpy.ops.script.execute_preset(
            filepath=
            "C:\\Program Files\\Blender Foundation\\Blender 2.92\\2.92\\scripts\\presets\\interface_theme\\blender_light.xml",
            menu_idname="USERPREF_MT_interface_theme_presets")  # TODO 自动检测版本，以适应路径
        bpy.ops.preferences.addon_enable(module="node_wrangler")
        bpy.ops.preferences.addon_enable(module="object_fracture_cell")
        bpy.ops.preferences.addon_enable(module="render_auto_tile_size")
        bpy.ops.preferences.addon_enable(module="development_icon_get")
        userpref.inputs.use_rotate_around_active = True
        userpref.inputs.use_zoom_to_mouse = True
        context.window_manager.keyconfigs['blender'].preferences[
            'use_pie_click_drag'] = True
        context.window_manager.keyconfigs['blender'].preferences[
            'use_v3d_shade_ex_pie'] = True

        userpref.addons['cycles'].preferences.compute_device_type = "CUDA"
        #userpref.addons['cycles'].preferences.devices[0].use = True # 一般显卡会自动启用。
        #userpref.addons['cycles'].preferences.devices[1].use = True
        userpref.system.audio_device = "SDL"

        userpref.filepaths.use_file_compression = True
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


ClassName = (
    ButtonUI,
    ToggleButtonFunction,
    HintScheme,
    HintSchemeDeveloper,
    HintSchemeDefault,
    SettingsMenu,
    MyPreferences,
)

lang_dict = {
    "zh_CN": {
        "toggle_button": "切换",
        "settings_menu": "设置",
        "hint_scheme": "提示方案",
        "hint_scheme_type_default": "提示方案：默认",
        "hint_scheme_type_developer": "提示方案：开发者",
        "hint_scheme_default": "默认",
        "hint_scheme_developer": "开发者",
        "new_data_translation": "新建数据 - 翻译",
        "my_preferences": "我的偏好设置"
    },
    "en_US": {
        "toggle_button": "Toggle",
        "settings_menu": "Settings",
        "hint_scheme": "Hint Scheme",
        "hint_scheme_type_default": "Hint Scheme: Default",
        "hint_scheme_type_developer": "Hint Scheme: Developer",
        "hint_scheme_default": "Default",
        "hint_scheme_developer": "Developer",
        "new_data_translation": "New Data - Translation",
        "my_preferences": "My Preferences"
    }
}
