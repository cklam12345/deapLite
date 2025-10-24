Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "runfrontend_ssl.bat" & Chr(34), 0
Set WshShell = Nothing
