; filepath: /c:/Users/kaike/Desktop/Tablet/hidecursor.ahk
#NoEnv
#Persistent
SetWorkingDir %A_ScriptDir%

global flag := false

; Auto-elevate script
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

ToggleCursor()
{
    global flag
    if (flag)
        RestoreCursor()
    else
        HideCursor()
    flag := !flag
}

HideCursor()
{
    VarSetCapacity(AndMask, 128, 0xFF)
    VarSetCapacity(XorMask, 128, 0)
    
    CursorIDs := [32512, 32650, 32515, 32649, 32651, 32513, 32648, 32646, 32643, 32645, 32642, 32644, 32516, 32514]
    
    Loop % CursorIDs.Length()
    {
        CursorID := CursorIDs[A_Index]
        CursorHandle := DllCall("CreateCursor", "Ptr", 0, "Int", 0, "Int", 0, "Int", 32, "Int", 32, "Ptr", &AndMask, "Ptr", &XorMask)
        DllCall("SetSystemCursor", "Ptr", CursorHandle, "Int", CursorID)
    }
}

RestoreCursor()
{
    DllCall("SystemParametersInfo", "UInt", 0x57, "UInt", 0, "Ptr", 0, "UInt", 0)
}

; Auto toggle on start
ToggleCursor()
ExitApp