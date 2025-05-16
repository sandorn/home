; ------------------------------
; 参数初始化与热键配置
; ------------------------------
#SingleInstance Force          ; 禁止重复启动脚本
#MaxThreadsPerHotkey 2         ; 允许热键中断循环
global isInterrupted := false  ; 中断标志变量

; 启动连续点击（Ctrl+3）
^3::
    isInterrupted := false     ; 重置中断状态
    totalClicks := 100         ; 总点击次数
    Progress, P0, 正在点击（剩余次数：%totalClicks%）, 自动点击进度, AutoClick
    Loop %totalClicks% {
        if (isInterrupted) {
            Break              ; 检测中断标志
        }
        try {
            Click
        } catch e {
            MsgBox 点击失败：%e%
            Break
        }
        ; Sleep 30
        remaining := totalClicks - A_Index  ; 计算剩余次数
        Progress, % A_Index, 正在点击（剩余次数：%remaining%）
    }
    Progress, Off
Return

; 新增：中断循环（Ctrl+4）
^4::
    isInterrupted := true      ; 触发中断
    ToolTip 已暂停点击（按Ctrl+3继续）
    SetTimer, RemoveToolTip, 2000
Return

RemoveToolTip:
    ToolTip
Return

; 强制退出脚本（Esc）
Esc::ExitApp
