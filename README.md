
# ✂️📋 ClipGPT

ClipGPT is a Python-based tool that allows you to interact with **OpenAI GPT-4o-mini** directly using your clipboard. Whether it's text or images, you can copy content and send it to GPT with a simple shortcut. Responses are also logged for future reference.

---

## ✨ Features
- 🚀 **Send text or images** directly from your clipboard to OpenAI's GPT-4o-mini.
- 📂 **Log all interactions** (text and images) in a local file for easy access.
- 🖼️ **Supports text and image inputs** (Base64 encoded for images).
- 🛠️ **Lightweight and efficient**: Uses simple keyboard shortcuts for seamless interaction.

---

## 📋 Prerequisites

1. Install **Python 3.8+**.
2. Install the required Python packages:
   ```bash
   pip install openai pyperclip keyboard python-dotenv pillow
   ```
3. Create a file named `.env` in the project directory and configure your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   You can find your API key in your OpenAI account settings: [OpenAI API Keys](https://platform.openai.com/settings/).

---

## 🛠️ Installation

1. Clone or download this repository.
2. Navigate to the project directory:
   ```bash
   cd ClipGPT
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your OpenAI API key with these paraneters:
   Name: OPENAI_API_KEY
   Value: [paste your key]
   1. The `.env` file as described above if you want to run it through a terminal.
   2. Environment Variables (eg: Windows->Edit Environment Variables for your account->New)

---

## 🖥️ Usage

1. **Run the script:**
   - To run the file without showing a terminal window, use:
     ```bash
     pythonw clip-gpt.py
     ```
     Or provide the full path to the Python executable:
     ```bash
     C:\Users\gaulerie\AppData\Local\Programs\Python\Python312\pythonw.exe [location of file]
     ```

2. **Shortcuts**:
   - **Copy text or image**: Use `Ctrl + C` as usual to copy content to your clipboard.
   - **Send to GPT**: Press `Alt + C` to send the current clipboard content (text or image) to GPT.
   - **Exit the script**: Press `Ctrl + Q`.

3. **Logs**:
   - All interactions (text and image) are saved in a file called `ChatGPT_History_Log.txt` located in your `Documents` folder.

---

## 📝 Example Workflow

1. Copy **"What is the capital of France?"** to your clipboard with `Ctrl + C`.
2. Press `Alt + C` to send the question to GPT.
3. The response **"The capital of France is Paris."** is copied back to your clipboard and logged in `ChatGPT_History_Log.txt`.

For images:
1. Copy an image to your clipboard (e.g., using a screenshot tool).
2. Press `Alt + C` to analyze the image with GPT.

---

## 📂 File Structure

- **`clip-gpt.py`**: Main script file.
- **`.env`**: Contains your API key.
- **`ChatGPT_History_Log.txt`**: Logs all interactions (created in the `Documents` folder).

---

## ⚠️ Notes

- Ensure that your clipboard content is either text or an image; unsupported formats may cause errors.
- The API token should remain private. Do not share your `.env` file.
- Logs are stored locally; ensure you manage them securely if sensitive information is involved.

---

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes!

---

## 📜 License

This project is licensed under the MIT License.
