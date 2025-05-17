## ClipGPT: Interact with OpenAI via Clipboard

An invisible Python tool to query the OpenAI API using clipboard content. Supports both text and images (Base64). Logs all interactions locally.

---

### Features

* Supports clipboard text and image (Base64)
* Keyboard shortcut-based UI
* Logs queries and replies locally
* Automatically reuses document context across a session:
  * For PDFs: uses OpenAI file upload (with `file_id`)
  * For Excel, CSV, DOCX, TXT: extracts and resends structured text
  * For images: uses Vision input format with `image_url`

---

### Prerequisites

* **Executable:** Just download and run `clip-gpt.exe`
* **Manual:**

  * Python 3.8+
  * Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
  * Set environment variables:

    **Windows:**

    * `OPENAI_API_KEY=your_key`
    * `GPT_MODEL=model_name` *(optional)*
    * `GPT_PROMPT=your_prompt` *(optional)*
    * `CONTINUOUS_CONVERSATION=true or false` *(default false)*

    **Linux/macOS:** Add to shell profile (`~/.bashrc`, `~/.zshrc`, etc):

    ```bash
    export OPENAI_API_KEY="your_key"
    export GPT_MODEL="model_name"
    export GPT_PROMPT="your_prompt"
    source ~/.bashrc
    ```

---

### Installation

```bash
git clone https://github.com/... && cd ClipGPT
pip install -r requirements.txt
```

---

### Usage

* **Executable:** Run `clip-gpt.exe`, operates in background
* **Manual:**

  ```bash
  pythonw clip-gpt.pyw
  ```
* **Shortcuts:**

  * `Alt + C` → Send clipboard to GPT
  * `Ctrl + Q` → Quit

Logs saved to `ChatGPT_History_Log.csv` in Documents.

---

### Notes

* Only clipboard text/images supported
* Logs may contain sensitive data
* API key security is your responsibility
* PDF context is preserved via file ID (not memory)
* Image URLs are handled using GPT Vision input

---

### License

Distributed under the [LICENSE](LICENSE.md).
Feel free to open an issue or pull request if you have any questions, requests, or want to contribute.