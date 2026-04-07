from ai.client import AIClient
from input.screen import capture_screen

client = AIClient()
while True:
    text = input("")
    if text == "exit":
        break
    screen = capture_screen()
    messages = [{"role": "user", "content": [
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": screen,
        }
    },
    {
        "type": "text",
        "text": text
    }
    ]}]
    reply = client.chat(messages)
    print(reply)