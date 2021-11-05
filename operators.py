import bpy
from bpy.types import Operator
from bpy.app import translations
from multiprocessing import cpu_count


def message_box(title="Message Box", message="", icon="INFO"):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw,
                                          title=translations.pgettext(title),
                                          icon=icon)


class TOGGLE_LANGUAGE_OT_toggle_language(Operator):
    bl_idname = "toggle_language.toggle_language"
    bl_label = "Toggle"
    bl_description = "Click button to toggle language"

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
            message_box(
                title="Fail to Toggle Language",
                message=
                "Two languages are same! Please select two different languages for addon.",
                icon="ERROR")
        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_use_default_hint_scheme(Operator):
    bl_idname = "toggle_language.use_default_hint_scheme"
    bl_label = "Default Mode"
    bl_description = "Show no extra information"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = False
        userpref.view.show_tooltips_python = False
        self.report({"INFO"}, "Switch to default mode!")
        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_use_developer_hint_scheme(Operator):
    bl_idname = "toggle_language.use_developer_hint_scheme"
    bl_label = "Developer Mode"
    bl_description = "Show tooltips and options for developers"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = True
        userpref.view.show_tooltips_python = True
        self.report({"INFO"}, "Switch to developer mode!")
        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_load_my_settings(Operator):
    bl_idname = "toggle_language.load_my_settings"
    bl_label = "Load My Settings"
    bl_description = "Load my customized settings of startup file and preferences"

    def execute(self, context):
        scene = context.scene
        userpref = context.preferences
        addonpref = userpref.addons["ToggleLanguage"].preferences

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

        if addonpref.disable_theme_setting == False:
            user_platform = bpy.app.build_platform
            execution_path = bpy.app.binary_path
            theme_path = "{First_Main_Number}.{Second_Main_Number}/scripts/presets/interface_theme/" + blender_light_theme_name
            theme_path = theme_path.format(
                First_Main_Number=userpref.version[0],
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
        else:
            pass

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
        if addonpref.disable_paths_setting == False:
            userpref.filepaths.use_auto_save_temporary_files = False
            userpref.filepaths.texture_directory = "H:/Textures/"
            userpref.filepaths.temporary_directory = "E:/Temp/"
            userpref.filepaths.render_cache_directory = "E:/Temp/"
            userpref.filepaths.render_output_directory = "E:/Process/"
            scene.render.filepath = "E:/Process/"
        else:
            pass

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


class TOGGLE_LANGUAGE_OT_load_factory_settings(Operator):
    bl_idname = "toggle_language.load_factory_settings"
    bl_label = "Load Factory Settings"
    bl_description = "Load factory settings of startup file and preferences"

    def execute(self, context):
        bpy.ops.wm.read_factory_settings()
        bpy.ops.wm.save_userpref()
        bpy.ops.wm.save_homefile()
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


classes = (
    TOGGLE_LANGUAGE_OT_toggle_language,
    TOGGLE_LANGUAGE_OT_use_default_hint_scheme,
    TOGGLE_LANGUAGE_OT_use_developer_hint_scheme,
    TOGGLE_LANGUAGE_OT_load_my_settings,
    TOGGLE_LANGUAGE_OT_load_factory_settings,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
