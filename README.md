
# 🤖 ChatGPT Windows Automation Script

This AutoIt script allows you to quickly interact with ChatGPT by selecting text from any application and sending it to ChatGPT. The script runs in the background, pastes the selected text into ChatGPT, copies the response, and pastes it back into the clipboard for easy access.

🔗 **GitHub Repository:** [ungaul/chatgpt-windows](https://github.com/ungaul/chatgpt-windows)

## 🚀 Features

- **Select and Send**: Select text in any window, press `Ctrl + Shift + G`, and the text will be sent to ChatGPT.
- **Clipboard Response**: The response from ChatGPT is automatically copied to your clipboard for easy access.
- **Hotkey to Close**: You can close the script and the ChatGPT window anytime by pressing `Ctrl + Shift + H`.
- **Runs in Background**: The ChatGPT window is moved off-screen, so the process runs invisibly without disturbing your workspace.

## 🛠 Installation

1. **Install AutoIt**:
   - Download and install [AutoIt](https://www.autoitscript.com/site/autoit/downloads/). This tool is necessary to run the script.

2. **Download the Script**:
   - Download or clone this repository from GitHub:
     ```bash
     git clone https://github.com/ungaul/chatgpt-windows.git
     ```
   - Save the script as `chatgpt_windows.au3`.

3. **Run the Script**:
   - To run the script, simply double-click the `.au3` file, or use the AutoIt editor to launch it.

## 💻 How to Use

### ✨ Sending Text to ChatGPT
1. **Select Text**:
   - In any window, select the text you'd like to send to ChatGPT.
   
2. **Press the Hotkey**:
   - Press `Ctrl + Shift + G` to trigger the script.
   
3. **Wait for the Response**:
   - The script will send the text to ChatGPT and wait 10 seconds for a response.

4. **Response Copied to Clipboard**:
   - The response is automatically copied to your clipboard, ready to paste wherever needed. You can access it with `Win + V` to view your clipboard history.

### ❌ Closing the Script
- Press `Ctrl + Shift + H` to close both the script and the ChatGPT window.

## 🔧 How It Works

1. **Opens ChatGPT in a New Window**:
   - The script opens a new Chrome window with a specific ChatGPT conversation link.

2. **Text Interaction**:
   - After selecting the text, pressing the hotkey (`Ctrl + Shift + G`) will copy the selected text, paste it into ChatGPT, and send the message.
   
3. **Waits for Response**:
   - After 10 seconds, the script uses ChatGPT's built-in shortcut (`Ctrl + Shift + C`) to copy the response.

4. **Copies to Clipboard**:
   - The response from ChatGPT is automatically copied to your clipboard for further use.

5. **Closes Cleanly**:
   - By pressing `Ctrl + Shift + H`, the ChatGPT window is focused and closed properly, and the script stops running.

## 📋 Requirements

- **AutoIt**: You must have AutoIt installed to run the script.
- **Google Chrome**: The script uses Chrome to interact with ChatGPT. Ensure it's installed on your system.

## 🔑 Hotkeys

- **`Ctrl + Shift + G`**: Send selected text to ChatGPT.
- **`Ctrl + Shift + H`**: Close the script and the ChatGPT window.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
