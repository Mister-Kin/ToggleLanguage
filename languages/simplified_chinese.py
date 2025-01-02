langs_dict = {
    "zh_HANS": {
        # __init.py
        ("*", "Toggle Language"): "切换语言",
        (
            "*",
            "One click to toggle UI between two languages",
        ): "在两种语言中一键切换界面语言",
        ("*", "Topbar Menu"): "顶部菜单栏",
        # ui.py
        ("*", "Settings"): "设置",
        ("*", "Current Hint Scheme: Default"): "当前提示方案：默认",
        ("*", "Current Hint Scheme: Developer"): "当前提示方案：开发者",
        ("*", "Hint Scheme Menu"): "提示方案菜单",
        # operators.py
        ("*", "Message Box"): "消息框",
        ("Operator", "Toggle Language"): "切换语言",
        ("*", "Click button to toggle language"): "点击按钮以切换语言",
        ("*", "Switched to"): "已切换到",
        ("*", "interface!"): "界面！",
        ("*", "Fail to Toggle Language"): "切换语言失败",
        (
            "*",
            "Two languages are same! Please select two different languages for addon.",
        ): "两种语言相同！请为插件选择两种不同的语言。",
        ("Operator", "Default Mode"): "默认模式",
        ("*", "Show no extra information"): "不显示多余的信息",
        ("*", "Switched to default mode!"): "已切换到默认模式！",
        ("Operator", "Developer Mode"): "开发者模式",
        ("*", "Show tooltips and options for developers"): "显示开发者的工具提示和选项",
        ("*", "Switched to developer mode!"): "已切换到开发者模式！",
        ("Operator", "Load My Blender Settings"): "加载我的Blender设置",
        (
            "*",
            "Load my customized blender settings for startup file and preferences",
        ): "加载我的Blender启动文件和偏好设置的自定义设置",
        (
            "*",
            "This will load my customized blender settings for startup file and preferences. It might change your current settings for startup file and preferences. Are you sure?",
        ): "这将会加载我的Blender启动文件和偏好设置的自定义设置。它可能会改变你当前的启动文件和偏好设置。你确定吗？",
        ("*", "Load My Blender Settings"): "加载我的Blender设置",
        ("Operator", "Load Blender Factory Settings"): "加载Blender初始设置",
        (
            "*",
            "Load blender factory default startup file and preferences",
        ): "还原blender启动文件和默认偏好设置",
        (
            "*",
            "This will load blender factory default startup file and preferences. It will completely restore every blender setting to default value, not just addon settings. Are you sure?",
        ): "这将会还原blender启动文件和默认偏好设置。它将完全恢复每个Blender设置项到默认值，不仅仅是插件设置。你确定吗？",
        ("*", "Load Factory Settings"): "加载初始设置",
        (
            "Operator",
            "Delete All Collections and Objects in Current Scene",
        ): "删除当前场景中的所有集合和物体",
        (
            "*",
            "Delete all collections and objects in current scene",
        ): "删除当前场景中的所有集合和物体",
        (
            "*",
            "Delete all collections and objects in current scene successfully!",
        ): "成功删除当前场景中的所有集合和物体！",
        (
            "*",
            "This will delete all collections and objects in current scene. Are you sure?",
        ): "这将删除当前场景中的所有集合和物体。你确定吗？",
        ("*", "Delete All"): "全部删除",
        ("Operator", "Add Video Progress Bar"): "添加视频进度条",
        (
            "*",
            "Add video progress bar depend on current scene settings",
        ): "根据当前场景设置，添加视频进度条",
        ("*", "video progress bar bottom mask"): "视频进度条底遮罩",
        ("*", "video progress bar roll mask"): "视频进度条滚动遮罩",
        ("*", "video progress bar mask"): "视频进度条遮罩",
        ("*", "Add video progress bar successfully!"): "成功添加视频进度条！",
        ("Operator", "Import Blueprint (Reference Image)"): "导入蓝图（参考图）",
        (
            "*",
            "Import blueprint (reference image) to current scene",
        ): "导入蓝图（参考图）到当前场景",
        ("*", "Fail to Import Blueprint (Reference Image)"): "无法导入蓝图（参考图）",
        (
            "*",
            "Haven't selected any reference images! Please re-import and select some reference images.",
        ): "没有选择任何参考图像！请重新导入并选择一些参考图像。",
        ("*", "Blueprint"): "蓝图",
        ("*", "Blueprint Front"): "蓝图前视图",
        ("*", "Blueprint Rear"): "蓝图后视图",
        ("*", "Blueprint Right"): "蓝图右视图",
        ("*", "Blueprint Left"): "蓝图左视图",
        ("*", "Blueprint Top"): "蓝图俯视图",
        ("*", "Blueprint Bottom"): "蓝图仰视图",
        (
            "*",
            "Import blueprint (reference image) successfully!",
        ): "成功导入蓝图（参考图）！",
        # properties.py
        ("*", "Translate New Data-Block's Name"): "翻译新建数据块的名称",
        (
            "*",
            "Enable or disable translation for new data-block's name",
        ): "启用或禁用新建数据块名称的翻译",
        ("*", "First Language"): "第一种语言",
        ("*", "First language for toggling"): "用于切换的第一种语言",
        ("*", "Second Language"): "第二种语言",
        ("*", "Second language for toggling"): "用于切换的第二种语言",
        ("*", "Disable Paths Setting"): "禁用路径设置",
        (
            "*",
            "Disable paths setting for Load My Blender Settings feature",
        ): "禁用“加载我的Blender设置”功能的路径设置",
        ("*", "Disable Theme Setting"): "禁用主题设置",
        (
            "*",
            "Disable theme setting for Load My Blender Settings feature",
        ): "禁用“加载我的Blender设置”功能的主题设置",
        ("*", "Disable Saving Startup File"): "禁止保存启动文件",
        (
            "*",
            "Disable saving startup file when applying feature Load My Blender Settings",
        ): "应用“加载我的Blender设置”功能时，禁止保存启动文件",
        (
            "*",
            "Please select two languages for addon to toggle UI language.",
        ): "请为插件选择两种语言以用于切换界面语言。",
        (
            "*",
            "Addon's Keymaps",
        ): "插件的键位映射",
        (
            "*",
            "Some settings for Load My Blender Settings feature.",
        ): "一些关于“加载我的Blender设置”功能的设置。",
        (
            "*",
            "Please configure following settings before applying Load My Blender Settings feature.",
        ): "在应用“加载我的Blender设置”功能前，请配置以下设置。",
        ("*", "Use CPU in GPU Render Setting"): "在GPU渲染设置中使用CPU",
        (
            "*",
            "Use CPU in GPU render setting for Load My Blender Settings feature",
        ): "在“加载我的Blender设置”功能的GPU渲染设置中使用CPU",
        ("*", "Enable Selection for Import Blueprint"): "启用“导入蓝图”的选择",
        (
            "*",
            "Enable selection for Import Blueprint feature",
        ): "启用“导入蓝图”功能的选择",
        ("*", "Addon's Utility Settings"): "插件的实用工具设置",
        ("*", "Preset Theme"): "预设主题",
        (
            "*",
            "Preset theme for Load My Blender Settings feature",
        ): "“加载我的Blender设置”功能的预设主题",
        ("*", "Blender Dark (Dark Theme)"): "Blender深（深色主题）",
        ("*", "Blender Light (Light Theme)"): "Blender浅（浅色主题）",
        ("*", "Deep Grey (Dark Theme)"): "深灰（深色主题）",
        ("*", "Maya (Dark Theme)"): "Maya（深色主题）",
        ("*", "Minimal Dark (Dark Theme)"): "小深（深色主题）",
        ("*", "Modo (Dark Theme)"): "Modo（深色主题）",
        ("*", "Print Friendly (Light Theme)"): "适合打印（浅色主题）",
        ("*", "White (Light Theme)"): "白色（浅色主题）",
        ("*", "XSI (Light Theme)"): "XSI（浅色主题）",
    }
}

langs_dict["zh_CN"] = langs_dict["zh_HANS"]
