from ai.client import AIClient
client = AIClient()
while True:
    text = input("")
    if text == "exit":
        break
    messages = [{"role": "user", "content": text}]
    reply = client.chat(messages)
    print(reply)