import bpy
from bpy.types import PropertyGroup, AddonPreferences
from bpy.props import BoolProperty, EnumProperty
from bpy.app import translations
import rna_keymap_ui
from . import keymaps

enum_languages = (
    ("zh_HANS", "Simplified Chinese (简体中文)", "zh_HANS", 1),
    ("zh_HANT", "Traditional Chinese (繁體中文)", "zh_HANT", 2),
    ("en_US", "English (English)", "en_US", 3),
    ("ca_AD", "Catalan (Català)", "ca_AD", 4),
    ("es", "Spanish (Español)", "es", 5),
    ("fr_FR", "French (Français)", "fr_FR", 6),
    ("ja_JP", "Japanese (日本語)", "ja_JP", 7),
    ("sk_SK", "Slovak (Slovenčina)", "sk_SK", 8),
    ("cs_CZ", "Czech (Čeština)", "cs_CZ", 9),
    ("de_DE", "German (Deutsch)", "de_DE", 10),
    ("it_IT", "Italian (Italiano)", "it_IT", 11),
    ("ka", "Georgian (ქართული)", "ka", 12),
    ("ko_KR", "Korean (한국어)", "ko_KR", 13),
    ("pt_BR", "Brazilian Portuguese (Português do Brasil)", "pt_BR", 14),
    ("pt_PT", "Portuguese (Português)", "pt_PT", 15),
    ("ru_RU", "Russian (Русский)", "ru_RU", 16),
    ("uk_UA", "Ukrainian (Українська)", "uk_UA", 17),
    ("vi_VN", "Vietnamese (Tiếng Việt)", "vi_VN", 18),
)

enum_languages_before_v4 = (
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
        userpref.view.use_translate_new_dataname = (
            scene.toggle_language_settings.translate_new_dataname
        )


class Toggle_Language_settings(PropertyGroup):
    translate_new_dataname: BoolProperty(
        name="Translate New Data-Block's Name",
        description="Enable or disable translation for new data-block's name",
        default=False,
        update=update_translate_new_dataname_state,
    )


class Toggle_Language_preferences(AddonPreferences):
    bl_idname = __package__

    # 在 AddonPreferences class 中构建 property，其值才能随着用户偏好设置自动保存。
    first_lang: EnumProperty(
        name="First Language",
        description="First language for toggling",
        default="zh_HANS",
        items=enum_languages,
    )

    first_lang_before_v4: EnumProperty(
        name="First Language",
        description="First language for toggling",
        default="zh_CN",
        items=enum_languages_before_v4,
    )

    second_lang: EnumProperty(
        name="Second Language",
        description="Second language for toggling",
        default="en_US",
        items=enum_languages,
    )

    second_lang_before_v4: EnumProperty(
        name="Second Language",
        description="Second language for toggling",
        default="en_US",
        items=enum_languages_before_v4,
    )

    preset_theme: EnumProperty(
        name="Preset Theme",
        description="Preset theme for Load My Blender Settings feature",
        default="white",
        items=enum_themes,
    )

    disable_paths_setting: BoolProperty(
        name="Disable Paths Setting",
        description="Disable paths setting for Load My Blender Settings feature",
        default=False,
    )

    disable_theme_setting: BoolProperty(
        name="Disable Theme Setting",
        description="Disable theme setting for Load My Blender Settings feature",
        default=False,
    )

    disable_saving_startup_file: BoolProperty(
        name="Disable Saving Startup File",
        description="Disable saving startup file when applying feature Load My Blender Settings",
        default=False,
    )

    use_cpu_in_gpu_render_setting: BoolProperty(
        name="Use CPU in GPU Render Setting",
        description="Use CPU in GPU render setting for Load My Blender Settings feature",
        default=False,
    )

    enable_selection_for_import_blueprint: BoolProperty(
        name="Enable Selection for Import Blueprint",
        description="Enable selection for Import Blueprint feature (Blueprint reference can't be selected after importing if not checked)",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        userpref = context.preferences

        box = layout.box()
        box.label(
            text="Please select two languages for addon to toggle UI language.",
            icon="SETTINGS",
        )
        row = box.row(align=True)
        if userpref.version[0] >= 4:
            row.prop(self, "first_lang")
            row.separator()
            row.prop(self, "second_lang")
        else:
            row.prop(self, "first_lang_before_v4")
            row.separator()
            row.prop(self, "second_lang_before_v4")

        box = layout.box()
        box.label(
            text="Addon's Keymaps",
            icon="TOOL_SETTINGS",
        )
        col = box.column()
        kc = bpy.context.window_manager.keyconfigs.addon
        # km = context.window_manager.keyconfigs.user.keymaps["Window"]
        for km, kmi in keymaps.addon_keymaps:
            km = km.active()
            kmi = self.get_addon_keymaps_item(km, kmi.idname)
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)

        box = layout.box()
        box.label(
            text="Addon's Utility Settings",
            icon="TOOL_SETTINGS",
        )
        row = box.row(align=True)
        row.prop(self, "enable_selection_for_import_blueprint")

        box = layout.box()
        box.label(
            text="Some settings for Load My Blender Settings feature.",
            icon="TOOL_SETTINGS",
        )
        box.label(
            text="Please configure following settings before applying Load My Blender Settings feature.",
        )
        row = box.row(align=True)
        row.prop(self, "disable_paths_setting")
        row.separator()
        row.prop(self, "disable_theme_setting")

        row = box.row(align=True)
        row.prop(self, "disable_saving_startup_file")
        row.separator()
        row.prop(self, "use_cpu_in_gpu_render_setting")

        row = box.row(align=True)
        row.prop(self, "preset_theme")

    def get_addon_keymaps_item(self, km, kmi_idname):
        for i, km_item in enumerate(km.keymap_items):
            if km.keymap_items.keys()[i] == kmi_idname:
                return km_item
        return None


classes = (
    Toggle_Language_settings,
    Toggle_Language_preferences,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.toggle_language_settings = bpy.props.PointerProperty(
        type=Toggle_Language_settings
    )


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)

    del bpy.types.Scene.toggle_language_settings
