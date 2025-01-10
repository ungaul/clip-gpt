import openai
import pyperclip
import keyboard
import time
import os
import base64
import io
from PIL import ImageGrab
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini"

log_file_path = os.path.join(os.environ["USERPROFILE"], "Documents", "ChatGPT_History_Log.txt")

def log_interaction(input_type, content, response):
    """Logs the interaction into the log file."""
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()} - {input_type.upper()}\n")
        if input_type == "text":
            log_file.write(f"Input: {content}\n")
        else:
            log_file.write("Input: Image (Base64 encoded)\n")
        log_file.write(f"Response: {response}\n")
        log_file.write("-" * 50 + "\n")

def send_to_openai(content, is_image=False):
    """Sends the content to GPT-4o-mini and returns the response."""
    try:
        if is_image:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this image and provide concise information."},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{content}"}
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Provide concise and clean responses for academic purposes."},
                    {"role": "user", "content": content}
                ]
            )
        return response.choices[0].message.content
    except Exception as e:
        print("API Error:", e)
        return "Error: Could not generate a response."

def encode_image_from_clipboard():
    """Encodes the image in the clipboard as a Base64 string."""
    try:
        image = ImageGrab.grabclipboard()
        if image:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return encoded_image
        return None
    except Exception as e:
        print("Image Encoding Error:", e)
        return None

def monitor_clipboard():
    print("Monitoring clipboard. Use Alt+C to send text or image to GPT-4o-mini. Press Ctrl+Q to exit.")
    while True:
        if keyboard.is_pressed("ctrl+q"):
            print("Exiting...")
            break
        if keyboard.is_pressed("alt+c"):
            time.sleep(0.5)
            content = pyperclip.paste()
            encoded_image = encode_image_from_clipboard()
            if encoded_image:
                print("Alt+C detected. Sending image to GPT-4o-mini...")
                response = send_to_openai(encoded_image, is_image=True)
                pyperclip.copy(response)
                log_interaction("image", encoded_image, response)
                print("Response copied to clipboard.")
            elif content.strip():
                print("Alt+C detected. Sending text to GPT-4o-mini...")
                response = send_to_openai(content)
                pyperclip.copy(response)
                log_interaction("text", content, response)
                print("Response copied to clipboard.")
            else:
                print("Clipboard is empty.")
        time.sleep(0.1)

if __name__ == "__main__":
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            log_file.write("ChatGPT Interaction History Log\n")
            log_file.write("=" * 50 + "\n")
    monitor_clipboard()
