; 鼠标连点器脚本 (AutoHotkey v2版本)
; 作者：AI助手
; 创建时间：2024年
; 版本：1.1

; 全局配置
class Config {
    static clickInterval := 10 ; 默认点击间隔（毫秒）
    static clickButton := "Left" ; 默认点击按钮（Left, Right, Middle）
    static useCurrentPosition := true ; 使用当前鼠标位置
    static customX := 0 ; 自定义X坐标（仅当useCurrentPosition为false时生效）
    static customY := 0 ; 自定义Y坐标（仅当useCurrentPosition为false时生效）
    static showClickCount := true ; 显示点击次数
}

; 全局状态变量
class State {
    static isClicking := false
    static isPaused := false
    static clickCount := 0
    static startTime := 0
}

; 热键设置
^1::StartClicking() ; Ctrl+1 开始点击
^2::StopClicking()  ; Ctrl+2 停止点击
^3::TogglePause()   ; Ctrl+3 切换暂停/继续
^4::ShowSettings()  ; Ctrl+4 显示设置
^0::ExitApp        ; Ctrl+0 退出程序

; 开始点击函数
StartClicking() {
    if (State.isClicking) {
        ToolTip("点击已经在运行中")
        SetTimer(RemoveToolTip, -1500)
        return
    }
    
    State.isClicking := true
    State.isPaused := false
    State.clickCount := 0
    State.startTime := A_TickCount
    
    ToolTip("开始点击 - 间隔: " Config.clickInterval "ms")
    SetTimer(RemoveToolTip, -1500)
    
    ClickLoop()
}

; 停止点击函数
StopClicking() {
    if (!State.isClicking) {
        ToolTip("没有正在运行的点击任务")
        SetTimer(RemoveToolTip, -1500)
        return
    }
    
    State.isClicking := false
    State.isPaused := false
    
    duration := Round((A_TickCount - State.startTime) / 1000, 1)
    ToolTip("已停止点击 - 总点击数: " State.clickCount " - 持续时间: " duration "秒")
    SetTimer(RemoveToolTip, -3000)
}

; 切换暂停/继续函数
TogglePause() {
    if (!State.isClicking) {
        ToolTip("没有正在运行的点击任务")
        SetTimer(RemoveToolTip, -1500)
        return
    }
    
    if (State.isPaused) {
        State.isPaused := false
        ClickLoop()
        ToolTip("继续点击")
    } else {
        State.isPaused := true
        ToolTip("已暂停点击 - 当前点击数: " State.clickCount)
    }
    SetTimer(RemoveToolTip, -1500)
}

; 点击循环函数
ClickLoop() {
    if (State.isClicking && !State.isPaused) {
        ; 执行点击
        if (Config.useCurrentPosition) {
            Click(Config.clickButton)
        } else {
            Click(Config.customX, Config.customY, Config.clickButton)
        }
        
        ; 更新点击计数
        State.clickCount++
        
        ; 定期更新托盘提示显示点击次数
        if (Config.showClickCount && Mod(State.clickCount, 100) == 0) {
            UpdateTrayTip()
        }
        
        ; 继续循环
        SetTimer(ClickLoop, Config.clickInterval)
    }
}

; 更新托盘提示
UpdateTrayTip() {
    A_TrayTip := "鼠标连点器 - 点击数: " State.clickCount 
        . (State.isPaused ? " (已暂停)" : "")
        . " - Ctrl+1开始, Ctrl+2停止, Ctrl+3暂停/继续, Ctrl+4设置, Ctrl+0退出"
}

; 显示设置对话框
ShowSettings() {
    static settingsGui := 0
    
    if (!settingsGui) {
        try {
            settingsGui := Gui("+Resize +MinSize300x200", "鼠标连点器设置")
        } catch as e {
            MsgBox("无法创建设置窗口: " e.Message, "错误", 16)
            return
        }
        
        ; 点击间隔
        settingsGui.Add("Text", "x10 y10 w80", "点击间隔(ms):")
        settingsGui.Add("Edit", "x100 y10 w100 vInterval", Config.clickInterval)
        
        ; 点击按钮
        settingsGui.Add("Text", "x10 y40 w80", "点击按钮:")
        buttonDDL := settingsGui.Add("DropDownList", "x100 y40 w100 vButton", ["Left", "Right", "Middle"])
        buttonDDL.Text := Config.clickButton
        
        ; 位置设置
        settingsGui.Add("Text", "x10 y70 w80", "点击位置:")
        settingsGui.Add("GroupBox", "x10 y90 w280 h80", "位置选择")
        radioUseCurrent := settingsGui.Add("Radio", "x30 y110 vUseCurrent Checked", "使用当前鼠标位置")
        radioUseCustom := settingsGui.Add("Radio", "x30 y135 vUseCustom", "自定义位置")
        
        ; 自定义坐标输入框
        settingsGui.Add("Text", "x80 y135 w20", "X:")
        settingsGui.Add("Edit", "x100 y135 w50 vCustomX Disabled", Config.customX)
        settingsGui.Add("Text", "x160 y135 w20", "Y:")
        settingsGui.Add("Edit", "x180 y135 w50 vCustomY Disabled", Config.customY)
        btnGetPos := settingsGui.Add("Button", "x240 y130 w40", "获取")
        
        ; 显示点击次数
        settingsGui.Add("CheckBox", "x10 y180 w150 vShowCount Checked", "显示点击次数")
        
        ; 应用按钮
        btnApply := settingsGui.Add("Button", "x100 y210 w80", "应用")
        btnCancel := settingsGui.Add("Button", "x200 y210 w80", "取消")
        
        ; 设置事件处理
        radioUseCurrent.OnEvent("Click", (*) => TogglePositionOptions(settingsGui, true))
        radioUseCustom.OnEvent("Click", (*) => TogglePositionOptions(settingsGui, false))
        btnGetPos.OnEvent("Click", (*) => GetCurrentMousePosition(settingsGui))
        btnApply.OnEvent("Click", (*) => ApplySettings(settingsGui))
        btnCancel.OnEvent("Click", (*) => settingsGui.Hide())
    }
    
    ; 更新GUI值
    settingsGui["Interval"].Text := Config.clickInterval
    settingsGui["Button"].Text := Config.clickButton
    settingsGui["UseCurrent"].Value := Config.useCurrentPosition ? 1 : 0
    settingsGui["UseCustom"].Value := Config.useCurrentPosition ? 0 : 1
    settingsGui["CustomX"].Text := Config.customX
    settingsGui["CustomY"].Text := Config.customY
    settingsGui["ShowCount"].Value := Config.showClickCount ? 1 : 0
    
    ; 启用/禁用自定义位置输入框
    settingsGui["CustomX"].Enabled := !Config.useCurrentPosition
    settingsGui["CustomY"].Enabled := !Config.useCurrentPosition
    
    settingsGui.Show()
}

; 切换位置选项
TogglePositionOptions(gui, useCurrent) {
    gui["CustomX"].Enabled := !useCurrent
    gui["CustomY"].Enabled := !useCurrent
}

; 获取当前鼠标位置
GetCurrentMousePosition(gui) {
    MouseGetPos(&x, &y)
    gui["CustomX"].Text := x
    gui["CustomY"].Text := y
}

; 应用设置
ApplySettings(gui) {
    ; 验证并保存设置
    try {
        interval := Integer(gui["Interval"].Text)
        if (interval < 1) {
            throw ValueError("间隔必须大于0")
        }
    } catch {
        MsgBox("请输入有效的点击间隔（大于0的整数）", "输入错误", 48)
        gui["Interval"].Focus()
        return
    }
    
    Config.clickInterval := interval
    Config.clickButton := gui["Button"].Text
    Config.useCurrentPosition := gui["UseCurrent"].Value
    Config.showClickCount := gui["ShowCount"].Value
    
    if (!Config.useCurrentPosition) {
        try {
            x := Integer(gui["CustomX"].Text)
            y := Integer(gui["CustomY"].Text)
        } catch {
            MsgBox("请输入有效的坐标值", "输入错误", 48)
            gui["CustomX"].Focus()
            return
        }
        Config.customX := x
        Config.customY := y
    }
    
    gui.Hide()
    ToolTip("设置已应用")
    SetTimer(RemoveToolTip, -1500)
}

; 移除提示
RemoveToolTip() {
    ToolTip()
}

; 托盘图标设置
try {
    A_TrayMenu.SetIcon("Shell32.dll", 43) ; 尝试设置托盘图标
} catch {
    ; 如果失败，使用默认图标或不设置图标
    ToolTip("托盘图标设置失败: " A_LastError)
    SetTimer(RemoveToolTip, -1500)
}
UpdateTrayTip() ; 初始化托盘提示

; 显示启动信息
ShowStartupInfo() {
    SplashText("鼠标连点器已启动：", "Ctrl+1: 开始点击 | Ctrl+2: 停止点击 | Ctrl+3: 暂停/继续 | Ctrl+4: 设置 | Ctrl+0: 退出", 400, 120)
    SetTimer(() => SplashText(), -2000)
}

; SplashText函数定义 - 使用AutoHotkey v2语法
SplashText(text1:="", text2:="", width:=200, height:=100) {
    static splashGui := 0
    
    if (splashGui && !text1) { ; 如果调用时没有参数，则隐藏窗口
        splashGui.Hide()
        return
    }
    
    if (!splashGui) {
        ; 创建GUI窗口
        try {
            splashGui := Gui("+ToolWindow +NoActivate +AlwaysOnTop", "Splash")
            splashGui.MarginX := 10
            splashGui.MarginY := 10
        } catch {
            ; 如果GUI创建失败，尝试使用MsgBox替代
            if (text1) {
                MsgBox(text1 "`n" text2, "提示", 64)
            }
            return
        }
        
        ; 添加标题文本
        try {
            titleCtrl := splashGui.Add("Text", "x10 y10 w" (width-20) " Center c0x0000FF", text1)
            titleCtrl.SetFont("s12 Bold")
        } catch {
            ; 如果添加控件失败，使用MsgBox替代
            if (text1) {
                MsgBox(text1 "`n" text2, "提示", 64)
            }
            return
        }
        
        ; 添加内容文本
        try {
            splashGui.Add("Text", "x10 y+10 w" (width-20) " Center", text2)
        } catch {
            ; 如果添加控件失败，使用MsgBox替代
            if (text1) {
                MsgBox(text1 "`n" text2, "提示", 64)
            }
            return
        }
    } else {
        ; 更新现有文本内容
        try {
            controls := splashGui.GetControls()
            if (controls.Length >= 1 && text1)
                controls[1].Text := text1
            if (controls.Length >= 2 && text2)
                controls[2].Text := text2
        } catch {
            ; 如果更新失败，使用MsgBox替代
            if (text1) {
                MsgBox(text1 "`n" text2, "提示", 64)
            }
            return
        }
    }
    
    ; 显示窗口
    try {
        splashGui.Show("w" width " h" height)
        ; 居中显示
        WinGetPos(,, &screenWidth, &screenHeight, "A")
        x := (screenWidth - width) // 2
        y := (screenHeight - height) // 2
        splashGui.Move(x, y)
    } catch {
        ; 如果显示失败，使用MsgBox替代
        if (text1) {
            MsgBox(text1 "`n" text2, "提示", 64)
        }
    }
}



; 启动时显示信息
ShowStartupInfo()