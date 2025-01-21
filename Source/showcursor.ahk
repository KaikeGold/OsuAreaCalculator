#NoEnv
#Persistent
SetWorkingDir %A_ScriptDir%

RestoreCursor()
{
    DllCall("SystemParametersInfo", "UInt", 0x57, "UInt", 0, "Ptr", 0, "UInt", 0)
}

RestoreCursor()
ExitApp