import bpy
from bpy.types import PropertyGroup, AddonPreferences
from bpy.props import BoolProperty, EnumProperty
from bpy.app import translations

enum_languages = (
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
    ("ru_RU", "Russian (Русский)", "ru_RU", 17),
)

enum_themes = (
    ("blender_dark", "Blender Dark", "Blender Dark (Dark Theme)", 1),
    ("blender_light", "Blender Light", "Blender Light (Light Theme)", 2),
    ("deep_grey", "Deep Grey", "Deep Grey (Dark Theme)", 3),
    ("maya", "Maya", "Maya (Dark Theme)", 4),
    ("minimal_dark", "Minimal Dark", "Minimal Dark (Dark Theme)", 5),
    ("modo", "Modo", "Modo (Dark Theme)", 6),
    ("print_friendly", "Print Friendly", "Print Friendly (Light Theme)", 7),
    ("white", "White", "White (Light Theme)", 8),
    ("xsi", "XSI", "XSI (Light Theme)", 9),
)


def update_translate_new_dataname_state(self, context):
    userpref = context.preferences
    scene = context.scene
    lang = translations.locale
    if lang != "en_US":
        userpref.view.use_translate_new_dataname = scene.toggle_language_settings.translate_new_dataname


class ToggleLanguageSettings(PropertyGroup):
    translate_new_dataname: BoolProperty(
        name="Translate New Data-Block's Name",
        description="Enable or disable translation of new data-block's name",
        default=False,
        update=update_translate_new_dataname_state,
    )


class ToggleLanguagePreferences(AddonPreferences):
    bl_idname = __package__

    # 在 AddonPreferences class 中构建 property，其值才能随着用户偏好设置自动保存。
    first_lang: EnumProperty(
        name="First Language",
        description="First language for toggling",
        default="zh_CN",
        items=enum_languages,
    )

    second_lang: EnumProperty(
        name="Second Language",
        description="Second language for toggling",
        default="en_US",
        items=enum_languages,
    )

    preset_theme: EnumProperty(
        name="Preset Theme",
        description="Preset theme for Load My Settings feature",
        default="white",
        items=enum_themes,
    )

    disable_paths_setting: BoolProperty(
        name="Disable Paths Setting",
        description="Disable paths setting of Load My Settings feature",
        default=False,
    )

    disable_theme_setting: BoolProperty(
        name="Disable Theme Setting",
        description="Disable theme setting of Load My Settings feature",
        default=False,
    )

    disable_saving_startup_file: BoolProperty(
        name="Disable Saving Startup File",
        description=
        "Disable saving startup file when applying feature Load My Settings",
        default=False,
    )

    use_cpu_in_gpu_render_setting: BoolProperty(
        name="Use CPU in GPU Render Setting",
        description="Use CPU in GPU render setting of Load My Settings feature",
        default=False,
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(
            text="Please select two languages for addon to toggle UI language.",
            icon="SETTINGS",
        )
        row = box.row(align=True)
        row.prop(self, "first_lang")
        row.separator()
        row.prop(self, "second_lang")

        box = layout.box()
        box.label(
            text="Some settings about Load My Settings feature.",
            icon="TOOL_SETTINGS",
        )
        box.label(
            text=
            "Please configure following settings before applying Load My Settings feature.",
        )
        row = box.row(align=True)
        row.prop(self, "disable_paths_setting")
        row.separator()
        row.prop(self, "disable_theme_setting")

        row = box.row(align=True)
        row.prop(self, "use_cpu_in_gpu_render_setting")
        row.separator()
        row.prop(self, "disable_saving_startup_file")

        row = box.row(align=True)
        row.prop(self, "preset_theme")


classes = (
    ToggleLanguageSettings,
    ToggleLanguagePreferences,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.toggle_language_settings = bpy.props.PointerProperty(
        type=ToggleLanguageSettings)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    del bpy.types.Scene.toggle_language_settings
