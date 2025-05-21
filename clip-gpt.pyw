import os
import openai
import pyperclip
import keyboard
import time
import io
import csv
import requests
import uuid
import pandas as pd
from docx import Document
from PIL import ImageGrab, Image
from datetime import datetime

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL", "gpt-4o")
prompt = os.getenv("GPT_PROMPT", "")
continuous_conversation = os.getenv("CONTINUOUS_CONVERSATION", "false").lower() == "true"
log_file_path = os.path.join(os.environ["USERPROFILE"], "Documents", "ChatGPT_History_Log.csv")

conversation_id = str(uuid.uuid4())
chat_history = []
active_context_reference = None
previous_model_reply = None

def log_interaction(input_type, content, response, used_model, usage):
    header = [
        "timestamp", "conversation_id", "input_type", "model", "input", "output",
        "tokens_prompt", "tokens_completion", "tokens_total"
    ]
    new_file = not os.path.exists(log_file_path)
    with open(log_file_path, "a", encoding="utf-8-sig", newline='') as log_file:
        writer = csv.writer(log_file)
        if new_file:
            writer.writerow(header)
        writer.writerow([
            datetime.now().isoformat(),
            conversation_id,
            input_type.upper(),
            used_model,
            content,
            response.strip(),
            usage.get("prompt_tokens", ""),
            usage.get("completion_tokens", ""),
            usage.get("total_tokens", "")
        ])

def extract_file_content(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".txt":
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext in [".csv", ".xlsx"]:
            df = pd.read_excel(path) if ext == ".xlsx" else pd.read_csv(path)
            return df.head(50).to_string(index=False)
        elif ext == ".docx":
            doc = Document(path)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        print(f"Error extracting from {path}: {e}")
    return None

def upload_pdf(path):
    try:
        uploaded = client.files.create(file=open(path, "rb"), purpose="user_data")
        return uploaded.id
    except Exception as e:
        print(f"PDF upload failed: {e}")
        return None

def is_supported_file(path):
    supported = [".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"]
    return os.path.isfile(path) and os.path.splitext(path)[1].lower() in supported

def upload_clipboard_image():
    try:
        grabbed = ImageGrab.grabclipboard()
        if isinstance(grabbed, Image.Image):
            image = grabbed.convert("RGB")
            image.thumbnail((512, 512))
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=80)
            buffer.seek(0)
            files = {'file': ('clip.jpg', buffer, 'image/jpeg')}
        elif isinstance(grabbed, list) and grabbed and os.path.isfile(grabbed[0]):
            files = {'file': open(grabbed[0], 'rb')}
        else:
            return None
        headers = {"User-Agent": "curl/7.64.1"}
        r = requests.post("https://0x0.st", files=files, headers=headers)
        return r.text.strip() if r.ok else None
    except Exception:
        return None

def send_to_openai(user_input, structured=False):
    global chat_history, active_context_reference, previous_model_reply
    messages = []

    if structured and active_context_reference:
        ctx = active_context_reference
        if ctx["type"] == "pdf":
            messages = [{
                "role": "user",
                "content": [
                    {"type": "file", "file": {"file_id": ctx["file_id"]}},
                    {"type": "text", "text":
                        (f'Previous reply: "{previous_model_reply.strip()}"\n' if previous_model_reply else '') +
                        f"User input: {user_input.strip()}"}
                ]
            }]
            kwargs = {"max_completion_tokens": 300}

        elif ctx["type"] == "image":
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input.strip() or "What's in this image?"},
                    {"type": "image_url", "image_url": {"url": ctx["url"]}}
                ]
            }]
            kwargs = {"max_completion_tokens": 300}

        elif ctx["type"] == "text":
            context_text = f'Context from {ctx["filename"]}:\n{ctx["content"].strip()}\n\n'
            if previous_model_reply:
                context_text += f'Previous reply: "{previous_model_reply.strip()}"\n'
            context_text += f"User input: {user_input.strip()}"
            messages = [{"role": "user", "content": context_text}]
            kwargs = {}

    else:
        messages = [{"role": "user", "content": user_input.strip()}]
        kwargs = {}

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )

    result = response.choices[0].message.content
    usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else {}

    if active_context_reference and active_context_reference.get("type") != "image":
        previous_model_reply = result

    return result, model, usage

def handle_clipboard():
    global active_context_reference, previous_model_reply
    time.sleep(0.2)
    text = pyperclip.paste().strip().strip('"')
    image_url = upload_clipboard_image()

    if image_url:
        print("Alt+C detected. Sending image to GPT...")
        active_context_reference = {"type": "image", "url": image_url}
        previous_model_reply = None
        response, used_model, usage = send_to_openai("", structured=True)
        pyperclip.copy(response)
        log_interaction("image", image_url, response, used_model, usage)
        print(f"Response copied to clipboard. Model: {used_model} | Tokens: {usage}")
        return

    if is_supported_file(text):
        ext = os.path.splitext(text)[1].lower()
        filename = os.path.basename(text)
        print(f"Detected document path: {text}")

        if ext == ".pdf":
            file_id = upload_pdf(text)
            if file_id:
                active_context_reference = {"type": "pdf", "file_id": file_id, "filename": filename}
                previous_model_reply = None
                response, used_model, usage = send_to_openai("Please analyze this PDF.", structured=True)
                pyperclip.copy(response)
                log_interaction("document", text, response, used_model, usage)
                print(f"Response copied to clipboard. Model: {used_model} | Tokens: {usage}")
            else:
                print("PDF upload failed.")
        else:
            content = extract_file_content(text)
            if content:
                active_context_reference = {"type": "text", "content": content, "filename": filename}
                previous_model_reply = None
                response, used_model, usage = send_to_openai("Please analyze this document.")
                pyperclip.copy(response)
                log_interaction("document", text, response, used_model, usage)
                print(f"Response copied to clipboard. Model: {used_model} | Tokens: {usage}")
            else:
                print("Failed to extract text.")
        return

    if text.lower().startswith("http://") or text.lower().startswith("https://"):
        print("Alt+C detected. Sending URL to GPT...")
        response, model_used, usage = send_to_openai(text, structured=True)
        pyperclip.copy(response)
        log_interaction("document", text, response, model_used, usage)
        print(f"Response copied to clipboard. Model: {model_used} | Tokens: {usage}")
        return

    if text:
        print("Alt+C detected. Sending text to GPT...")
        response, model_used, usage = send_to_openai(text)
        pyperclip.copy(response)
        log_interaction("text", text, response, model_used, usage)
        print(f"Response copied to clipboard. Model: {model_used} | Tokens: {usage}")
        return

    print("Clipboard is empty or contains no valid data.")

def main():
    print("ClipGPT ready. Press Alt+C to send clipboard. Press Ctrl+Q to quit.")
    keyboard.add_hotkey("alt+c", handle_clipboard)
    while True:
        event = keyboard.read_event()
        if event.event_type == "down" and event.name == "q" and keyboard.is_pressed("ctrl"):
            print("Exiting ClipGPT.")
            break

if __name__ == "__main__":
    main()
