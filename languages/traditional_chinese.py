langs_dict = {
    "zh_HANT": {
        # __init.py
        ("*", "Toggle Language"): "切換語言",
        (
            "*",
            "One click to toggle UI between two languages",
        ): "在兩種語言中一鍵切換界面語言",
        ("*", "Topbar Menu"): "頂部菜單欄",
        # ui.py
        ("*", "Settings"): "設定",
        ("*", "Current Hint Scheme: Default"): "當前提示方案：默認",
        ("*", "Current Hint Scheme: Developer"): "當前提示方案：開發者",
        ("*", "Hint Scheme Menu"): "提示方案菜單",
        ("*", "Utilities"): "效用",
        # operators.py
        ("*", "Confirm"): "確認",
        ("*", "Message Box"): "消息框",
        ("Operator", "Toggle Language"): "切換語言",
        ("*", "Click button to toggle language"): "點擊按鈕以切換語言",
        ("*", "Switched to"): "已切換到",
        ("*", "interface!"): "界面！",
        ("*", "Fail to Toggle Language"): "切換語言失敗",
        (
            "*",
            "Two languages are same! Please select two different languages for addon.",
        ): "兩種語言相同！請爲插件選擇兩種不同的語言。",
        ("Operator", "Default Mode"): "默認模式",
        ("*", "Show no extra information"): "不顯示多餘的信息",
        ("*", "Switched to default mode!"): "已切換到默認模式！",
        ("Operator", "Developer Mode"): "開發者模式",
        ("*", "Show tooltips and options for developers"): "顯示開發者的工具提示和選項",
        ("*", "Switched to developer mode!"): "已切換到開發者模式！",
        ("Operator", "Load My Blender Settings"): "載入我的Blender設定",
        (
            "*",
            "Load my customized blender settings for startup file and preferences",
        ): "載入我的blender啓動文件和偏好設定的自定義設定",
        (
            "*",
            "This will load my customized blender settings for startup file and preferences. It might change your current settings for startup file and preferences. Are you sure?",
        ): "這將會載入我的Blender啓動文件和偏好設定的自定義設定。它可能會改變你當前的啓動文件和偏好設定。你確定嗎？",
        ("*", "Load My Blender Settings"): "載入我的Blender設定",
        ("Operator", "Load Blender Factory Settings"): "載入Blender出廠設定",
        (
            "*",
            "Load blender factory default startup file and preferences",
        ): "載入blender出廠預設的初始啓動檔案和偏好設定",
        (
            "*",
            "This will load blender factory default startup file and preferences. It will completely restore every blender setting to default value, not just addon settings. Are you sure?",
        ): "這將會載入blender出廠預設的初始啓動檔案和偏好設定。它將完全恢復每個blender設定項到預設值，不僅僅是插件設定。你確定嗎？",
        ("*", "Load Factory Settings"): "載入出廠設定",
        (
            "Operator",
            "Delete All Collections and Objects in Current Scene",
        ): "删除當前場景中的所有集合和物體",
        (
            "*",
            "Delete all collections and objects in current scene",
        ): "删除當前場景中的所有集合和物體",
        (
            "*",
            "Delete all collections and objects in current scene successfully!",
        ): "成功删除當前場景中的所有集合和物體！",
        (
            "*",
            "This will delete all collections and objects in current scene. Are you sure?",
        ): "這將删除當前場景中的所有集合和物體。你確定嗎？",
        ("*", "Delete All"): "全部刪除",
        ("Operator", "Add Video Progress Bar"): "添加視頻進度條",
        (
            "*",
            "Add video progress bar depend on current scene settings",
        ): "根據當前場景設定，添加視頻進度條",
        ("*", "video progress bar bottom mask"): "視頻進度條底遮罩",
        ("*", "video progress bar roll mask"): "視頻進度條滾動遮罩",
        ("*", "video progress bar mask"): "視頻進度條遮罩",
        ("*", "Add video progress bar successfully!"): "成功添加視頻進度條！",
        ("Operator", "Import Blueprint (Reference Image)"): "載入藍圖（參考圖）",
        (
            "*",
            "Import blueprint (reference image) to current scene",
        ): "載入藍圖（參考圖）到當前場景",
        ("*", "Fail to Import Blueprint (Reference Image)"): "無法載入藍圖（參考圖）",
        (
            "*",
            "Haven't selected any reference images! Please re-import and select some reference images.",
        ): "沒有選擇任何參考圖像！請重新載入並選擇一些參考圖像。",
        ("*", "Blueprint"): "藍圖",
        ("*", "Blueprint Front"): "藍圖前視圖",
        ("*", "Blueprint Rear"): "藍圖後視圖",
        ("*", "Blueprint Right"): "藍圖右視圖",
        ("*", "Blueprint Left"): "藍圖左視圖",
        ("*", "Blueprint Top"): "藍圖俯視圖",
        ("*", "Blueprint Bottom"): "藍圖仰視圖",
        (
            "*",
            "Import blueprint (reference image) successfully!",
        ): "成功載入藍圖（參考圖）！",
        ("Operator", "Check Addon Update"): "檢查插件更新",
        ("*", "Check for updates."): "檢查插件更新情況",
        ("*", "not found"): "未找到",
        (
            "*",
            "Current addon version can't be retrieved. Please check if",
        ): "無法檢索當前插件的版本。請檢查",
        ("*", "exists."): "是否存在。",
        (
            "*",
            "Addon updated successfully. Please restart Blender to finish update.",
        ): "插件更新成功。請重新啓動Blender以完成更新。",
        ("*", "Addon updated successfully"): "插件更新成功",
        (
            "*",
            "Please restart Blender to finish update.",
        ): "請重新啓動Blender以完成更新。",
        (
            "*",
            "Failed to download latest version of the addon.",
        ): "無法下載最新版本的插件。",
        ("*", "current_version: "): "當前版本：",
        ("*", "latest_version: "): "最新版本：",
        ("*", "Your addon is out-of-date."): "你的插件需要更新。",
        ("*", "Your addon is already up-to-date."): "你的插件已經是最新發佈版。",
        ("*", "Your addon is newer than latest."): "你的插件版本已超前于最新發佈版。",
        ("*", "Failed to retrieve latest version."): "無法檢索到最新版本。",
        # properties.py
        ("*", "Translate New Data-Block's Name"): "翻譯新建數據塊的名稱",
        (
            "*",
            "Enable or disable translation for new data-block's name",
        ): "啓用或禁用新建數據塊名稱的翻譯",
        ("*", "First Language"): "第一種語言",
        ("*", "First language for toggling"): "用於切換的第一種語言",
        ("*", "Second Language"): "第二種語言",
        ("*", "Second language for toggling"): "用於切換的第二種語言",
        ("*", "Disable Paths Setting"): "禁用路徑設定",
        (
            "*",
            "Disable paths setting for Load My Blender Settings feature",
        ): "禁用“載入我的Blender設定”功能的路徑設定",
        ("*", "Disable Theme Setting"): "禁用主題設定",
        (
            "*",
            "Disable theme setting for Load My Blender Settings feature",
        ): "禁用“載入我的Blender設定”功能的主題設定",
        ("*", "Disable Saving Startup File"): "禁止儲存初始啓動檔案",
        (
            "*",
            "Disable saving startup file when applying feature Load My Blender Settings",
        ): "應用“載入我的Blender設定”功能時，禁止儲存初始啓動檔案",
        (
            "*",
            "Please select two languages for addon to toggle UI language.",
        ): "請爲插件選擇兩種語言以用於切換界面語言。",
        (
            "*",
            "Addon's Keymaps",
        ): "插件的鍵位映射",
        (
            "*",
            "Some settings for Load My Blender Settings feature.",
        ): "一些關於“載入我的Blender設定”功能的設定。",
        (
            "*",
            "Please configure following settings before applying Load My Blender Settings feature.",
        ): "在應用“載入我的Blender設定”功能前，請配置以下設定。",
        ("*", "Use CPU in GPU Render Setting"): "在GPU渲染設定中使用CPU",
        (
            "*",
            "Use CPU in GPU render setting for Load My Blender Settings feature",
        ): "在“載入我的Blender設定”功能的GPU渲染設定中使用CPU",
        ("*", "Enable Selection for Import Blueprint"): "啓用“載入藍圖”的選擇",
        (
            "*",
            "Enable selection for Import Blueprint feature (Blueprint reference can't be selected after importing if not checked)",
        ): "啓用“載入藍圖”功能的選擇（若未勾選,則藍圖參考圖在載入後無法被選中）",
        ("*", "Addon's Utility Settings"): "插件的效用設定",
        ("*", "Preset Theme"): "預設主題",
        (
            "*",
            "Preset theme for Load My Blender Settings feature",
        ): "“載入我的Blender設定”功能的預設主題",
        ("*", "Blender Dark (Dark Theme)"): "Blender深（深色主題）",
        ("*", "Blender Light (Light Theme)"): "Blender浅（淺色主題）",
        ("*", "Deep Grey (Dark Theme)"): "深灰（深色主題）",
        ("*", "Maya (Dark Theme)"): "Maya（深色主題）",
        ("*", "Minimal Dark (Dark Theme)"): "小深（深色主題）",
        ("*", "Modo (Dark Theme)"): "Modo（深色主題）",
        ("*", "Print Friendly (Light Theme)"): "適合打印（淺色主題）",
        ("*", "White (Light Theme)"): "白色（淺色主題）",
        ("*", "XSI (Light Theme)"): "XSI（淺色主題）",
    }
}

langs_dict["zh_TW"] = langs_dict["zh_HANT"]
