import bpy
from bpy.types import Operator, OperatorFileListElement
from bpy.app import translations
from multiprocessing import cpu_count
from . import properties
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, CollectionProperty
from math import radians
import requests, os, io, json, shutil, zipfile, tempfile


class TOGGLE_LANGUAGE_OT_message_box_with_confirm(bpy.types.Operator):
    bl_idname = "wm.message_box_with_confirm"
    bl_label = "Message Box"

    title: bpy.props.StringProperty(default="Message Box")
    message: bpy.props.StringProperty(default="")
    icon: bpy.props.StringProperty(default="INFO")

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(
            self,
            event,
            title=self.title,
            message=self.message,
            confirm_text="Confirm",
            icon=self.icon,
        )


def message_box_with_confirm(title="Message Box", message="", icon="INFO"):
    bpy.ops.wm.message_box_with_confirm(
        "INVOKE_DEFAULT", title=title, message=message, icon=icon
    )


def message_box(title="Message Box", message="", icon="INFO"):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(
        draw, title=translations.pgettext(title), icon=icon
    )


class TOGGLE_LANGUAGE_OT_toggle_language(Operator):
    bl_idname = "toggle_language.toggle_language"
    bl_label = "Toggle Language"
    bl_description = "Click button to toggle language"

    def execute(self, context):
        userpref = context.preferences
        addonpref = userpref.addons[__package__].preferences
        lang = translations.locale

        if userpref.version[0] >= 4:
            if addonpref.first_lang != addonpref.second_lang:
                if lang == addonpref.first_lang:
                    userpref.view.language = addonpref.second_lang
                else:
                    userpref.view.language = addonpref.first_lang
                enum_languages_dict = {
                    lang[0]: lang[1] for lang in properties.enum_languages
                }
                self.report(
                    {"INFO"},
                    "{} {} {}".format(
                        translations.pgettext("Switched to"),
                        enum_languages_dict.get(userpref.view.language),
                        translations.pgettext("interface!"),
                    ),
                )
            else:
                userpref = bpy.context.preferences
                if (
                    userpref.version[0] == 4 and userpref.version[1] >= 1
                ) or userpref.version[0] >= 5:
                    message_box_with_confirm(
                        title="Fail to Toggle Language",
                        message="Two languages are same! Please select two different languages for addon.",
                        icon="ERROR",
                    )
                else:
                    message_box_with_confirm(
                        title="Fail to Toggle Language",
                        message="Two languages are same! Please select two different languages for addon.",
                        icon="ERROR",
                    )
        else:
            if addonpref.first_lang_before_v4 != addonpref.second_lang_before_v4:
                if lang == addonpref.first_lang_before_v4:
                    userpref.view.language = addonpref.second_lang_before_v4
                else:
                    userpref.view.language = addonpref.first_lang_before_v4
                enum_languages_before_v4_dict = {
                    lang[0]: lang[1] for lang in properties.enum_languages_before_v4
                }
                self.report(
                    {"INFO"},
                    "{} {} {}".format(
                        translations.pgettext("Switched to"),
                        enum_languages_before_v4_dict.get(userpref.view.language),
                        translations.pgettext("interface!"),
                    ),
                )
            else:
                userpref = bpy.context.preferences
                if (
                    userpref.version[0] == 4 and userpref.version[1] >= 1
                ) or userpref.version[0] >= 5:
                    message_box_with_confirm(
                        title="Fail to Toggle Language",
                        message="Two languages are same! Please select two different languages for addon.",
                        icon="ERROR",
                    )
                else:
                    message_box_with_confirm(
                        title="Fail to Toggle Language",
                        message="Two languages are same! Please select two different languages for addon.",
                        icon="ERROR",
                    )

        # 检测并修正 use_translate_new_dataname 选项值。
        scene = context.scene
        lang = translations.locale
        if lang != "en_US":
            if (
                userpref.view.use_translate_new_dataname
                != scene.toggle_language_settings.translate_new_dataname
            ):
                userpref.view.use_translate_new_dataname = (
                    scene.toggle_language_settings.translate_new_dataname
                )

        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_use_default_hint_scheme(Operator):
    bl_idname = "toggle_language.use_default_hint_scheme"
    bl_label = "Default Mode"
    bl_description = "Show no extra information"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = False
        userpref.view.show_tooltips_python = False
        self.report({"INFO"}, "Switched to default mode!")
        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_use_developer_hint_scheme(Operator):
    bl_idname = "toggle_language.use_developer_hint_scheme"
    bl_label = "Developer Mode"
    bl_description = "Show tooltips and options for developers"

    def execute(self, context):
        userpref = context.preferences

        userpref.view.show_developer_ui = True
        userpref.view.show_tooltips_python = True
        self.report({"INFO"}, "Switched to developer mode!")
        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_load_my_blender_settings(Operator):
    bl_idname = "toggle_language.load_my_blender_settings"
    bl_label = "Load My Blender Settings"
    bl_description = (
        "Load my customized blender settings for startup file and preferences"
    )

    def execute(self, context):
        scene = context.scene
        userpref = context.preferences
        addonpref = userpref.addons[__package__].preferences

        if userpref.version[1] >= 90:
            blender_v290 = True
        else:
            blender_v290 = False
        if userpref.version[0] >= 3:
            blender_v3_plus = True
            if (
                userpref.version[0] == 3 and userpref.version[1] >= 4
            ) or userpref.version[0] >= 4:
                blender_v34_plus = True
                if (
                    userpref.version[0] == 4 and userpref.version[1] >= 1
                ) or userpref.version[0] >= 5:
                    blender_v41_plus = True
                    if (
                        userpref.version[0] == 4
                        and userpref.version[1] >= 2
                        or userpref.version[0] >= 5
                    ):
                        blender_v42_plus = True
                        if (
                            userpref.version[0] == 4
                            and userpref.version[1] >= 5
                            or userpref.version[0] >= 5
                        ):
                            blender_v45_plus = True
                        else:
                            blender_v45_plus = False
                    else:
                        blender_v42_plus = False
                else:
                    blender_v41_plus = False
            else:
                blender_v34_plus = False
        else:
            blender_v3_plus = False

        # v2.93 及之后版本的文件命名有所变化。
        if blender_v42_plus:
            dict_blender_theme_name = {
                "blender_dark": "Blender_Dark.xml",
                "blender_light": "Blender_Light.xml",
                "deep_grey": "theme_deep_grey",
                "maya": "theme_maya",
                "minimal_dark": "theme_minimal_dark",
                "modo": "theme_modo",
                "print_friendly": "theme_print_friendly",
                "white": "theme_white",
                "xsi": "theme_xsi",
            }
            blender_keyconfig_name = "Blender"
        elif blender_v3_plus or userpref.version[1] == 93:
            dict_blender_theme_name = {
                "blender_dark": "Blender_Dark.xml",
                "blender_light": "Blender_Light.xml",
                "deep_grey": "Deep_Grey.xml",
                "maya": "Maya.xml",
                "minimal_dark": "Minimal_Dark.xml",
                "modo": "Modo.xml",
                "print_friendly": "Print_Friendly.xml",
                "white": "White.xml",
                "xsi": "XSI.xml",
            }
            blender_keyconfig_name = "Blender"
        else:
            dict_blender_theme_name = {
                "blender_dark": "blender_dark.xml",
                "blender_light": "blender_light.xml",
                "deep_grey": "deep_grey.xml",
                "maya": "maya.xml",
                "minimal_dark": "minimal_dark.xml",
                "modo": "modo.xml",
                "print_friendly": "print_friendly.xml",
                "white": "white.xml",
                "xsi": "xsi.xml",
            }
            blender_keyconfig_name = "blender"

        userpref.view.ui_scale = 1.3
        if blender_v290 or blender_v3_plus:
            userpref.view.show_statusbar_stats = True
            userpref.view.show_statusbar_memory = True
            if userpref.view.is_property_readonly("show_statusbar_vram"):
                pass  # 无显卡时，该属性为只读，无法对其进行写操作。
            else:
                userpref.view.show_statusbar_vram = True
        else:
            # v2.83 及之前版本未引入系统原生的 API，用 SDL 替代
            userpref.system.audio_device = "SDL"

        blender_theme_path_variable = {
            "blender_dark": "",
            "blender_light": "",
            "deep_grey": "addons/",
            "maya": "addons/",
            "minimal_dark": "addons/",
            "modo": "addons/",
            "print_friendly": "addons/",
            "white": "addons/",
            "xsi": "addons/",
        }

        user_platform = bpy.app.build_platform
        execution_path = bpy.app.binary_path
        if addonpref.disable_theme_setting == False:
            if (
                blender_v42_plus == True
                and addonpref.preset_theme != "blender_dark"
                and addonpref.preset_theme != "blender_light"
            ):
                bpy.ops.extensions.userpref_allow_online()
                bpy.ops.extensions.repo_sync_all()
                bpy.ops.extensions.package_install(
                    repo_index=0, pkg_id=dict_blender_theme_name[addonpref.preset_theme]
                )
            else:
                theme_path = (
                    "{First_Main_Number}.{Second_Main_Number}/scripts/"
                    + blender_theme_path_variable[addonpref.preset_theme]
                    + "presets/interface_theme/"
                    + dict_blender_theme_name[addonpref.preset_theme]
                )
                theme_path = theme_path.format(
                    First_Main_Number=userpref.version[0],
                    Second_Main_Number=userpref.version[1],
                )
                # b"Windows" b"Darwin" b"Linux"
                if user_platform == b"Windows":
                    theme_path = execution_path.replace("blender.exe", theme_path)
                elif user_platform == b"Darwin":
                    theme_path = execution_path.replace(
                        "MacOS/Blender", "Resources/" + theme_path
                    )
                else:
                    theme_path = execution_path[:-7] + theme_path
                bpy.ops.script.execute_preset(
                    filepath=theme_path,
                    menu_idname="USERPREF_MT_interface_theme_presets",
                )
        else:
            pass

        # 添加「视频剪辑」工作区
        video_editing_workspace_template_path = "{First_Main_Number}.{Second_Main_Number}/scripts/startup/bl_app_templates_system/Video_Editing/startup.blend"
        video_editing_workspace_template_path = (
            video_editing_workspace_template_path.format(
                First_Main_Number=userpref.version[0],
                Second_Main_Number=userpref.version[1],
            )
        )
        # b"Windows" b"Darwin" b"Linux"
        if user_platform == b"Windows":
            video_editing_workspace_template_path = execution_path.replace(
                "blender.exe", video_editing_workspace_template_path
            )
        elif user_platform == b"Darwin":
            video_editing_workspace_template_path = execution_path.replace(
                "MacOS/Blender", "Resources/" + video_editing_workspace_template_path
            )
        else:
            video_editing_workspace_template_path = (
                execution_path[:-7] + video_editing_workspace_template_path
            )
        # 追加并激活工作区为 Video Editing
        bpy.ops.workspace.append_activate(
            idname="Video Editing", filepath=video_editing_workspace_template_path
        )
        # 重新激活工作区为 Layout
        bpy.context.window.workspace = bpy.data.workspaces["Layout"]

        bpy.ops.preferences.addon_enable(module="node_wrangler")
        if blender_v42_plus:
            bpy.ops.extensions.package_install(repo_index=0, pkg_id="cell_fracture")
            bpy.ops.extensions.package_install(repo_index=0, pkg_id="icon_viewer")
        else:
            bpy.ops.preferences.addon_enable(module="object_fracture_cell")
            bpy.ops.preferences.addon_enable(module="development_icon_get")
        # v3.0 及之后版本用的是 cyclesX，其中的 Auto Tiles 功能是为了减少内存占用，
        # 即渲染 tile 大小的图像数据并缓存进硬盘，渲染结束时再合并在一起。
        # 与老版的 cycles 渲染调度逻辑不一样，因此 auto_tile_size 插件在 v3.0 中被移除。
        if blender_v3_plus:
            # TODO：根据当前可用内存自动设置合适大小（仍需查询资料或者查看源码确认显存是否会受影响）
            # 设置平铺大小为4096px，避免渲染4k图像时导致分割
            scene.cycles.tile_size = 4096
        else:
            bpy.ops.preferences.addon_enable(module="render_auto_tile_size")

        userpref.inputs.use_rotate_around_active = True
        userpref.inputs.use_zoom_to_mouse = True

        kcpref = context.window_manager.keyconfigs[blender_keyconfig_name].preferences
        kcpref.use_pie_click_drag = True
        kcpref.use_v3d_shade_ex_pie = True

        if blender_v45_plus:
            userpref.system.gpu_backend = "VULKAN"
            self.report(
                {"INFO"},
                "Please restart Blender to use Vulkan backend.",
            )

        userpref.filepaths.use_file_compression = True
        if addonpref.disable_paths_setting == False:
            # userpref.filepaths.use_auto_save_temporary_files = False
            userpref.filepaths.texture_directory = "H:/texture/"
            # userpref.filepaths.temporary_directory = "E:/temp/"
            # userpref.filepaths.render_cache_directory = "E:/temp/"
            userpref.filepaths.render_output_directory = "D:/process/"
            scene.render.filepath = "D:/process/"
        else:
            pass

        userpref.edit.undo_steps = 256

        # cycles渲染引擎设置
        scene.render.engine = "CYCLES"
        cpref = userpref.addons["cycles"].preferences
        if blender_v3_plus:
            cpref.refresh_devices()  # 刷新设备。
        else:
            cpref.get_devices()
        # 获取当前版本支持的设备类型，逐一设置以检测是否存在显卡。
        for device_type in cpref.get_device_types(bpy.context):
            try:
                cpref.compute_device_type = device_type[0]
                if cpref.has_active_device():
                    gpu_exist = True
                    # 当optix可用时优先选择。
                    if cpref.compute_device_type == "CUDA":
                        try:
                            cpref.compute_device_type = "OPTIX"
                            if cpref.has_active_device():
                                optix_exist = True
                                break
                            else:
                                optix_exist = False
                                cpref.compute_device_type = "CUDA"
                        except TypeError:
                            pass
                    break
                else:
                    gpu_exist = False
                    cpref.compute_device_type = "NONE"
            except TypeError:
                pass
        if gpu_exist:
            if blender_v3_plus:
                cpref.refresh_devices()  # 刷新设备。
            else:
                cpref.get_devices()
            for device in cpref.devices:
                if device.type == "CPU":
                    device.use = addonpref.use_cpu_in_gpu_render_setting
                else:
                    device.use = True
            scene.cycles.device = "GPU"
        else:
            pass
        if blender_v3_plus:
            if not gpu_exist and blender_v34_plus:
                scene.cycles.use_guiding = True
        else:
            scene.cycles.use_adaptive_sampling = True
            scene.cycles.adaptive_threshold = 0.1
            # render_auto_tile_size插件的tiles大小设置
            scene.ats_settings.gpu_choice = "128"

        # 渲染降噪设置
        if blender_v290 or blender_v3_plus:
            scene.cycles.use_denoising = True
            scene.cycles.use_preview_denoising = True
            scene.cycles.preview_denoising_input_passes = "RGB_ALBEDO_NORMAL"
            # gpu_exist为false时，根据短路求值原理，不会执行后面的语句。因此即使optix_exist未赋值时直接引用，也不会报错“UnboundLocalError: local variable 'optix_exist' referenced before assignment”
            if gpu_exist and optix_exist:
                if blender_v41_plus:
                    scene.cycles.denoiser = "OPENIMAGEDENOISE"
                    scene.cycles.denoising_use_gpu = True
                    scene.cycles.preview_denoiser = "OPENIMAGEDENOISE"
                    scene.cycles.preview_denoising_use_gpu = True
                    scene.cycles.preview_denoising_prefilter = "ACCURATE"
                else:
                    scene.cycles.denoiser = "OPTIX"
                    scene.cycles.preview_denoiser = "OPTIX"
            elif gpu_exist and not optix_exist:
                scene.cycles.denoiser = "OPENIMAGEDENOISE"
                scene.cycles.preview_denoiser = "OPENIMAGEDENOISE"
                scene.cycles.preview_denoising_prefilter = "ACCURATE"
                if blender_v41_plus:
                    scene.cycles.denoising_use_gpu = True
                    scene.cycles.preview_denoising_use_gpu = True
            elif blender_v290:
                scene.cycles.denoiser = "NLM"
                scene.cycles.preview_denoiser = "OPENIMAGEDENOISE"
            else:
                scene.cycles.denoiser = "OPENIMAGEDENOISE"
                scene.cycles.preview_denoiser = "OPENIMAGEDENOISE"
                scene.cycles.preview_denoising_prefilter = "ACCURATE"
        else:
            context.view_layer.cycles.use_denoising = True
            if gpu_exist and optix_exist:
                context.view_layer.cycles.use_optix_denoising = True
                context.view_layer.cycles.denoising_optix_input_passes = (
                    "RGB_ALBEDO_NORMAL"
                )
                scene.cycles.preview_denoising = "OPTIX"

        # cycles引擎采样设置
        scene.cycles.samples = 250
        scene.cycles.preview_samples = 1

        # 其他优化渲染速度的设置
        scene.render.use_persistent_data = True

        scene.render.threads_mode = "FIXED"
        scene.render.threads = max(1, cpu_count() - 2)
        bpy.ops.file.autopack_toggle()  # 自动打包资源，例如加载的外部纹理图片，避免路径改变后导致文件未找到
        bpy.ops.wm.save_userpref()
        if addonpref.disable_saving_startup_file == False:
            bpy.ops.wm.save_homefile()
        else:
            pass
        return {"FINISHED"}

    def invoke(self, context, event):
        userpref = bpy.context.preferences
        if (userpref.version[0] == 4 and userpref.version[1] >= 1) or userpref.version[
            0
        ] >= 5:
            return context.window_manager.invoke_confirm(
                self,
                event,
                message="This will load my customized blender settings for startup file and preferences. It might change your current settings for startup file and preferences. Are you sure?",
                confirm_text="Load My Blender Settings",
                icon="WARNING",
            )
        else:
            return context.window_manager.invoke_confirm(self, event)


class TOGGLE_LANGUAGE_OT_load_blender_factory_settings(Operator):
    bl_idname = "toggle_language.load_blender_factory_settings"
    bl_label = "Load Blender Factory Settings"
    bl_description = "Load blender factory default startup file and preferences"

    def execute(self, context):
        bpy.ops.wm.read_factory_settings()
        bpy.ops.wm.save_userpref()
        bpy.ops.wm.save_homefile()
        return {"FINISHED"}

    def invoke(self, context, event):
        userpref = bpy.context.preferences
        if (userpref.version[0] == 4 and userpref.version[1] >= 1) or userpref.version[
            0
        ] >= 5:
            return context.window_manager.invoke_confirm(
                self,
                event,
                message="This will load blender factory default startup file and preferences. It will completely restore every blender setting to default value, not just addon settings. Are you sure?",
                confirm_text="Load Factory Settings",
                icon="WARNING",
            )
        else:
            return context.window_manager.invoke_confirm(self, event)


class TOGGLE_LANGUAGE_OT_delete_all_collections_and_objects(Operator):
    bl_idname = "toggle_language.delete_all_collections_and_objects"
    bl_label = "Delete All Collections and Objects in Current Scene"
    bl_description = "Delete all collections and objects in current scene"

    def execute(self, context):
        scene = context.scene

        # 删除 Scene Collection 子项的物体
        for obj in scene.collection.objects:
            # if obj.users != 0可以检测data数据引用次数，不为0就删除，避免出现删除错误：which still has 1 users (including 0 'extra' shallow users)，实际测试无效
            bpy.data.objects.remove(obj)

        # 删除 Scene Collection 子项的集合，该操作也可直接删除子项集合中的物体
        for collection in scene.collection.children:
            bpy.data.collections.remove(collection)

        # remove会一同删除项目本身及其子项，但object的data还存储在blend文件中，可通过垃圾回收orphans_purge清除
        bpy.ops.outliner.orphans_purge(do_recursive=True)

        self.report(
            {"INFO"},
            "Delete all collections and objects in current scene successfully!",
        )
        return {"FINISHED"}

    def invoke(self, context, event):
        userpref = bpy.context.preferences
        if (userpref.version[0] == 4 and userpref.version[1] >= 1) or userpref.version[
            0
        ] >= 5:
            return context.window_manager.invoke_confirm(
                self,
                event,
                message="This will delete all collections and objects in current scene. Are you sure?",
                confirm_text="Delete All",
                icon="WARNING",
            )
        else:
            return context.window_manager.invoke_confirm(self, event)


# TODO：可调参数，弹出窗口，待完善开发
# TODO：首次完成添加视频进度条后，弹出可调参数窗口
# TODO：旁边按钮添加一个调出控制窗口的按钮
# class TOGGLE_LANGUAGE_OT_adjust_video_progress_bar(Operator):
#     bl_idname = "toggle_language.add_video_progress_bar"
#     bl_label = ""

#     def execute(self, context):

#         return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_add_video_progress_bar(Operator):
    bl_idname = "toggle_language.add_video_progress_bar"
    bl_label = "Add Video Progress Bar"
    bl_description = "Add video progress bar depend on current scene settings"

    def execute(self, context):
        scene = context.scene
        sequence_editor = scene.sequence_editor
        sequences = sequence_editor.sequences

        # 如果当前正在展开编辑meta片段就退出编辑，合闭meta片段元素，避免影响后续的选择创建meta片段
        # meta_stack[-1]倒数第一个元素就是当前展开编辑的meta片段
        if len(sequence_editor.meta_stack) > 0:
            bpy.ops.sequencer.meta_toggle()

        # 获取vse中没有片段最顶部的频道数字
        top_empty_channel_number = 0
        strips = sequence_editor.sequences_all
        for strip in strips:
            # 剔除meta子片段
            if strip.parent_meta() == None:
                if strip.channel > top_empty_channel_number:
                    top_empty_channel_number = strip.channel

        # 获取当前场景的设置
        start_frame = scene.frame_start
        end_frame = scene.frame_end

        if scene.toggle_language_settings.translate_new_dataname == False:
            name_text_bottom = "video progress bar bottom mask"
            name_text_roll = "video progress bar roll mask"
            name_text_meta = "video progress bar mask"
        else:
            name_text_bottom = translations.pgettext("video progress bar bottom mask")
            name_text_roll = translations.pgettext("video progress bar roll mask")
            name_text_meta = translations.pgettext("video progress bar mask")
        bottom_effect = sequences.new_effect(
            name=name_text_bottom,
            type="COLOR",
            channel=top_empty_channel_number + 1,
            frame_start=start_frame,
            frame_end=end_frame,
        )
        roll_effect = sequences.new_effect(
            name=name_text_roll,
            type="COLOR",
            channel=top_empty_channel_number + 2,
            frame_start=start_frame,
            frame_end=end_frame,
        )

        # 设置子进度条颜色
        bottom_effect.color = (0.45, 0.45, 0.45)
        roll_effect.color = (0.255, 0.255, 0.255)

        # 设置滚动遮罩层的关键帧动画
        date_path = "offset_x"
        roll_effect.transform.keyframe_insert(date_path, frame=start_frame)
        roll_effect.transform.offset_x = scene.render.resolution_x
        roll_effect.transform.keyframe_insert(date_path, frame=end_frame)

        bpy.ops.sequencer.select_all(action="DESELECT")
        effect_list = [bottom_effect, roll_effect]
        for effect in effect_list:
            effect.select = True
        bpy.ops.sequencer.meta_make()
        active_strip = sequence_editor.active_strip
        active_strip.name = name_text_meta
        active_strip.channel = top_empty_channel_number + 1
        # 裁切meta片段和设置透明度
        crop_value = scene.render.resolution_y - 44
        blend_alpha_value = 0.9
        active_strip.crop.min_y = crop_value
        active_strip.blend_alpha = blend_alpha_value
        active_strip.select = False

        # 强制刷新vse
        bpy.ops.sequencer.refresh_all()

        self.report({"INFO"}, "Add video progress bar successfully!")
        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_import_blueprint(Operator, ImportHelper):
    bl_idname = "toggle_language.import_blueprint"
    bl_label = "Import Blueprint (Reference Image)"
    bl_description = "Import blueprint (reference image) to current scene"

    filter_glob: StringProperty(
        # below line can support all image formats supported by blender
        # default="*" + ";*".join(bpy.path.extensions_image),
        default="*.png;*.jpg;*.jpeg;*.jp2;*.bmp;*.webp",
        options={"HIDDEN"},
        maxlen=255,
    )

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )

    directory: StringProperty(
        subtype="DIR_PATH",
    )

    def execute(self, context):
        files = self.files
        directory = self.directory
        if files[0].name == "":
            userpref = bpy.context.preferences
            if (
                userpref.version[0] == 4 and userpref.version[1] >= 1
            ) or userpref.version[0] >= 5:
                message_box_with_confirm(
                    title="Fail to Import Blueprint (Reference Image)",
                    message="Haven't selected any reference images! Please re-import and select some reference images.",
                    icon="ERROR",
                )
            else:
                message_box(
                    title="Fail to Import Blueprint (Reference Image)",
                    message="Haven't selected any reference images! Please re-import and select some reference images.",
                    icon="ERROR",
                )
        else:
            blueprint_path_front = blueprint_path_right = blueprint_path_top = (
                blueprint_path_rear
            ) = blueprint_path_left = blueprint_path_bottom = ""

            connector_list = ("-", "_", " ", ".")
            suffix_list_front = (
                "front",
                "frontview",
                "front-view",
                "front_view",
                "前",
                "前视",
                "前视图",
            )
            suffix_list_right = (
                "right",
                "rightview",
                "right-view",
                "right_view",
                "右",
                "右视",
                "右视图",
            )
            suffix_list_top = (
                "top",
                "topview",
                "top-view",
                "top_view",
                "俯",
                "俯视",
                "俯视图",
                "顶",
                "顶视",
                "顶视图",
            )
            suffix_list_rear = (
                "rear",
                "rearview",
                "rear-view",
                "rear_view",
                "后",
                "后视",
                "后视图",
            )
            suffix_list_left = (
                "left",
                "leftview",
                "left-view",
                "left_view",
                "左",
                "左视",
                "左视图",
            )
            suffix_list_bottom = (
                "bottom",
                "bottomview",
                "bottom-view",
                "bottom_view",
                "仰",
                "仰视",
                "仰视图",
            )

            for file in files:
                for connector in connector_list:
                    for suffix in suffix_list_front:
                        if connector + suffix in file.name:
                            blueprint_path_front = directory + file.name
                    for suffix in suffix_list_right:
                        if connector + suffix in file.name:
                            blueprint_path_right = directory + file.name
                    for suffix in suffix_list_top:
                        if connector + suffix in file.name:
                            blueprint_path_top = directory + file.name
                    for suffix in suffix_list_rear:
                        if connector + suffix in file.name:
                            blueprint_path_rear = directory + file.name
                    for suffix in suffix_list_left:
                        if connector + suffix in file.name:
                            blueprint_path_left = directory + file.name
                    for suffix in suffix_list_bottom:
                        if connector + suffix in file.name:
                            blueprint_path_bottom = directory + file.name

            blueprint_collection = bpy.data.collections.new(
                translations.pgettext("Blueprint")
            )
            userpref = context.preferences
            addonpref = userpref.addons[__package__].preferences
            if addonpref.enable_selection_for_import_blueprint == False:
                blueprint_collection.hide_select = True
            else:
                blueprint_collection.hide_select = False
            bpy.context.scene.collection.children.link(blueprint_collection)

            # 所有参考图缩放基准为前视图的高度，固定显示长度为4M。
            if blueprint_path_front != "":
                front_image_object = bpy.data.objects.new(
                    translations.pgettext("Blueprint Front"), None
                )
                blueprint_collection.objects.link(front_image_object)
                front_image_object.empty_display_type = "IMAGE"
                front_image = bpy.data.images.load(filepath=blueprint_path_front)
                front_image_object.data = front_image
                front_image_object.empty_display_size = 4
                front_width = front_image.size[0]
                front_height = front_image.size[1]
                if front_width > front_height:
                    scale = front_width / front_height
                    front_image_object.scale = (scale, scale, scale)
                front_image_object.location = (0, 4, 0)
                front_image_object.rotation_euler = (radians(90), 0, 0)
                front_image_object.empty_image_side = "FRONT"
                front_image_object.use_empty_image_alpha = True
                front_image_object.color[3] = 0.5
            if blueprint_path_rear != "":
                rear_image_object = bpy.data.objects.new(
                    translations.pgettext("Blueprint Rear"), None
                )
                blueprint_collection.objects.link(rear_image_object)
                rear_image_object.empty_display_type = "IMAGE"
                rear_image = bpy.data.images.load(filepath=blueprint_path_rear)
                rear_image_object.data = rear_image
                rear_image_object.empty_display_size = 4
                rear_width = rear_image.size[0]
                rear_height = rear_image.size[1]
                if rear_width > rear_height:
                    scale = rear_width / rear_height
                    rear_image_object.scale = (scale, scale, scale)
                rear_image_object.location = (0, -4, 0)
                rear_image_object.rotation_euler = (radians(90), 0, radians(180))
                rear_image_object.empty_image_side = "FRONT"
                rear_image_object.use_empty_image_alpha = True
                rear_image_object.color[3] = 0.5
            if blueprint_path_right != "":
                right_image_object = bpy.data.objects.new(
                    translations.pgettext("Blueprint Right"), None
                )
                blueprint_collection.objects.link(right_image_object)
                right_image_object.empty_display_type = "IMAGE"
                right_image = bpy.data.images.load(filepath=blueprint_path_right)
                right_image_object.data = right_image
                right_image_object.empty_display_size = 4
                right_width = right_image.size[0]
                right_height = right_image.size[1]
                if right_width > right_height:
                    scale = right_width / right_height
                    right_image_object.scale = (scale, scale, scale)
                right_image_object.location = (-4, 0, 0)
                right_image_object.rotation_euler = (radians(90), 0, radians(90))
                right_image_object.empty_image_side = "FRONT"
                right_image_object.use_empty_image_alpha = True
                right_image_object.color[3] = 0.5
            if blueprint_path_left != "":
                left_image_object = bpy.data.objects.new(
                    translations.pgettext("Blueprint Left"), None
                )
                blueprint_collection.objects.link(left_image_object)
                left_image_object.empty_display_type = "IMAGE"
                left_image = bpy.data.images.load(filepath=blueprint_path_left)
                left_image_object.data = left_image
                left_image_object.empty_display_size = 4
                left_width = left_image.size[0]
                left_height = left_image.size[1]
                if left_width > left_height:
                    scale = left_width / left_height
                    left_image_object.scale = (scale, scale, scale)
                left_image_object.location = (4, 0, 0)
                left_image_object.rotation_euler = (radians(90), 0, radians(-90))
                left_image_object.empty_image_side = "FRONT"
                left_image_object.use_empty_image_alpha = True
                left_image_object.color[3] = 0.5
            if blueprint_path_top != "":
                top_image_object = bpy.data.objects.new(
                    translations.pgettext("Blueprint Top"), None
                )
                blueprint_collection.objects.link(top_image_object)
                top_image_object.empty_display_type = "IMAGE"
                top_image = bpy.data.images.load(filepath=blueprint_path_top)
                top_image_object.data = top_image
                top_image_object.empty_display_size = 4
                top_width = top_image.size[0]
                top_height = top_image.size[1]
                if blueprint_path_front != "" or blueprint_path_rear != "":
                    if top_width > top_height:
                        if blueprint_path_front != "":
                            scale = (front_width / front_height) * (
                                top_width / top_height
                            )
                        else:
                            scale = (rear_width / rear_height) * (
                                top_width / top_height
                            )
                    else:
                        if blueprint_path_front != "":
                            scale = front_width / front_height
                        else:
                            scale = rear_width / rear_height
                    top_image_object.scale = (scale, scale, scale)
                elif blueprint_path_right != "" or blueprint_path_left != "":
                    if top_width > top_height:
                        if blueprint_path_right != "":
                            scale = right_width / right_height
                        else:
                            scale = left_width / left_height
                    else:
                        if blueprint_path_right != "":
                            scale = (right_width / right_height) * (
                                top_height / top_width
                            )
                        else:
                            scale = (left_width / left_height) * (
                                top_height / top_width
                            )
                    top_image_object.scale = (scale, scale, scale)
                top_image_object.location = (0, 0, -4)
                top_image_object.rotation_euler = (0, 0, radians(90))
                top_image_object.empty_image_side = "FRONT"
                top_image_object.use_empty_image_alpha = True
                top_image_object.color[3] = 0.5
            if blueprint_path_bottom != "":
                bottom_image_object = bpy.data.objects.new(
                    translations.pgettext("Blueprint Bottom"), None
                )
                blueprint_collection.objects.link(bottom_image_object)
                bottom_image_object.empty_display_type = "IMAGE"
                bottom_image = bpy.data.images.load(filepath=blueprint_path_bottom)
                bottom_image_object.data = bottom_image
                bottom_image_object.empty_display_size = 4
                bottom_width = bottom_image.size[0]
                bottom_height = bottom_image.size[1]
                if blueprint_path_front != "" or blueprint_path_rear != "":
                    if bottom_width > bottom_height:
                        if blueprint_path_front != "":
                            scale = (front_width / front_height) * (
                                bottom_width / bottom_height
                            )
                        else:
                            scale = (rear_width / rear_height) * (
                                bottom_width / bottom_height
                            )
                    else:
                        if blueprint_path_front != "":
                            scale = front_width / front_height
                        else:
                            scale = rear_width / rear_height
                    bottom_image_object.scale = (scale, scale, scale)
                elif blueprint_path_right != "" or blueprint_path_left != "":
                    if bottom_width > bottom_height:
                        if blueprint_path_right != "":
                            scale = right_width / right_height
                        else:
                            scale = left_width / left_height
                    else:
                        if blueprint_path_right != "":
                            scale = (right_width / right_height) * (
                                bottom_height / bottom_width
                            )
                        else:
                            scale = (left_width / left_height) * (
                                bottom_height / bottom_width
                            )
                    bottom_image_object.scale = (scale, scale, scale)
                bottom_image_object.location = (0, 0, 4)
                bottom_image_object.rotation_euler = (radians(180), 0, radians(90))
                bottom_image_object.empty_image_side = "FRONT"
                bottom_image_object.use_empty_image_alpha = True
                bottom_image_object.color[3] = 0.5
            self.report({"INFO"}, "Import blueprint (reference image) successfully!")
        return {"FINISHED"}


class TOGGLE_LANGUAGE_OT_check_addon_update(Operator):
    bl_idname = "toggle_language.check_addon_update"
    bl_label = "Check Addon Update"
    bl_description = "Check for updates."

    def get_current_addon_version(self, manifest_file):
        if os.path.exists(manifest_file):
            with open(manifest_file, "r") as f:
                content = f.read()
                lines = content.splitlines()
                version = None
                for line in lines:
                    if line.startswith("version = "):
                        version = line.split(" = ")[1].strip('"')
                        break
                return version
        else:
            userpref = bpy.context.preferences
            if (
                userpref.version[0] == 4 and userpref.version[1] >= 1
            ) or userpref.version[0] >= 5:
                message_box_with_confirm(
                    title=f"{manifest_file} {translations.pgettext('not found')}",
                    message="{} {} {}".format(
                        translations.pgettext(
                            "Current addon version can't be retrieved. Please check if"
                        ),
                        manifest_file,
                        translations.pgettext("exists."),
                    ),
                    icon="ERROR",
                )
            else:
                message_box(
                    title=f"{manifest_file} {translations.pgettext('not found')}",
                    message="{} {} {}".format(
                        translations.pgettext(
                            "Current addon version can't be retrieved. Please check if"
                        ),
                        manifest_file,
                        translations.pgettext("exists."),
                    ),
                    icon="ERROR",
                )
            return {"CANCELLED"}

    def download_and_install(self, latest_tag):
        url = f"https://github.com/Mister-Kin/ToggleLanguage/archive/refs/tags/{latest_tag}.zip"
        response = requests.get(url)
        if response.status_code == 200:
            zip_file_bytes = io.BytesIO(response.content)
            temp_dir = tempfile.gettempdir()
            with zipfile.ZipFile(zip_file_bytes) as zip_ref:
                zip_ref.extractall(temp_dir)
            latest_version = latest_tag.lstrip("v")
            latest_dir = os.path.join(temp_dir, f"ToggleLanguage-{latest_version}")
            current_dir = os.path.dirname(__file__)
            print(latest_dir, current_dir)
            shutil.rmtree(current_dir)
            shutil.copytree(latest_dir, current_dir, dirs_exist_ok=True, ignore=None)
            shutil.rmtree(latest_dir)
            # 暂未找到可靠方案实现自动刷新插件，因此需要手动重启Blender完成更新
            self.report(
                {"INFO"},
                "Addon updated successfully. Please restart Blender to finish update.",
            )
            userpref = bpy.context.preferences
            if (
                userpref.version[0] == 4 and userpref.version[1] >= 1
            ) or userpref.version[0] >= 5:
                message_box_with_confirm(
                    title="Addon updated successfully",
                    message="Please restart Blender to finish update.",
                    icon="INFO",
                )
            else:
                message_box(
                    title="Addon updated successfully",
                    message="Please restart Blender to finish update.",
                    icon="INFO",
                )
            return {"FINISHED"}
        else:
            self.report({"ERROR"}, "Failed to download latest version of the addon.")
            return {"CANCELLED"}

    def execute(self, context):

        current_dir = os.path.dirname(__file__)
        manifest_file = os.path.join(current_dir, "blender_manifest.toml")
        current_version = self.get_current_addon_version(manifest_file)
        addon_url = (
            "https://api.github.com/repos/Mister-Kin/ToggleLanguage/releases/latest"
        )
        response = requests.get(addon_url)
        if response.status_code == 200:
            data = json.loads(response.text)
            latest_tag = data["tag_name"]
            latest_version = latest_tag.lstrip("v")
            self.report(
                {"INFO"},
                f"{translations.pgettext('current_version: ')}{current_version}, {translations.pgettext('latest_version: ')}{latest_version}",
            )
            if latest_version > current_version:
                self.report({"INFO"}, "Your addon is out-of-date.")
                self.download_and_install(latest_tag)
                return {"FINISHED"}
            elif latest_version == current_version:
                self.report({"INFO"}, "Your addon is already up-to-date.")
                return {"CANCELLED"}
            else:
                self.report({"INFO"}, "Your addon is newer than latest.")
                return {"CANCELLED"}
        else:
            self.report({"ERROR"}, "Failed to retrieve latest version.")
            return {"CANCELLED"}


classes = (
    TOGGLE_LANGUAGE_OT_toggle_language,
    TOGGLE_LANGUAGE_OT_use_default_hint_scheme,
    TOGGLE_LANGUAGE_OT_use_developer_hint_scheme,
    TOGGLE_LANGUAGE_OT_load_my_blender_settings,
    TOGGLE_LANGUAGE_OT_load_blender_factory_settings,
    TOGGLE_LANGUAGE_OT_delete_all_collections_and_objects,
    TOGGLE_LANGUAGE_OT_add_video_progress_bar,
    TOGGLE_LANGUAGE_OT_import_blueprint,
    TOGGLE_LANGUAGE_OT_check_addon_update,
    TOGGLE_LANGUAGE_OT_message_box_with_confirm,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
