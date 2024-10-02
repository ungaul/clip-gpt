; Store the handle of the currently active window
Global $previousWindow = ""

; Function to click at specific coordinates (X, Y)
Func ClickAtCoords($xCoord, $yCoord)
    MouseClick("left", $xCoord, $yCoord)
    Sleep(500) ; Pause after each click to avoid errors
EndFunc

; Function to send the selected text to ChatGPT and copy the response back
Func SendToChatGPT()
    ; Save the handle of the current window (before switching to ChatGPT)
    $previousWindow = WinGetHandle("[ACTIVE]")

    ; Simulate Ctrl + C to copy the selected text
    Send("^c")
    Sleep(1000)

    WinActivate("Bot - Google Chrome") ; Activate the ChatGPT window based on title
    WinWaitActive("Bot - Google Chrome") ; Ensure the window becomes active
    Send("^v") ; Paste the copied text into ChatGPT
    Send("{ENTER}") ; Press Enter to send the request
    Sleep(10000) ; Wait for 10 seconds to get the response

    ; Use ChatGPT's shortcut Ctrl + Shift + C to copy the response
    Send("^+c")
    Sleep(1000)

    ; Return to the previously active window
    If $previousWindow <> "" Then
        WinActivate($previousWindow)
        WinWaitActive($previousWindow)
    EndIf

    ; Notify the user that the response is copied to the clipboard
EndFunc

; Function to close the script when Ctrl + Shift + H is pressed
Func CloseScript()
    ; Close the ChatGPT (Chrome) window
    WinActivate("Bot - Google Chrome") ; Activate the ChatGPT window based on title
    WinWaitActive("Bot - Google Chrome") ; Ensure the window becomes active
    WinClose("Bot - Google Chrome") ; Close the ChatGPT window
    Sleep(2000) ; Wait for the window to close

    ; Exit the script
    Exit
EndFunc

; Open the specific ChatGPT link in a new window
ShellExecute('C:\Program Files\Google\Chrome\Application\chrome_proxy.exe', '--profile-directory=Default --new-window https://chatgpt.com/c/66fcc0d2-1ae0-8005-91ae-d039fc699f95')
Sleep(5000) ; Wait for Chrome to load and the specific page to appear

; Maximize the Chrome window using AutoIt
WinWaitActive("[CLASS:Chrome_WidgetWin_1]") ; Wait for the ChatGPT window to be active
Sleep(2000)

; Move the window off-screen but still accessible (e.g., to coordinates -2000, 0)
WinMove("[CLASS:Chrome_WidgetWin_1]", "", 1920, 0) ; Move the window off-screen to the right (adjust the coordinates if necessary)
Sleep(1000)

; Set up a hotkey for Ctrl + Shift + G to trigger the interaction with ChatGPT
HotKeySet("^+g", "SendToChatGPT")

; Set up a hotkey for Ctrl + Shift + H to close the script and the ChatGPT window
HotKeySet("^+h", "CloseScript")

; Main loop to keep the script running and listening for the hotkeys
While 1
    Sleep(100)
WEnd
