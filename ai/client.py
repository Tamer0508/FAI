class AIClient:
    def __init__(self, provider: str = "ollama"): # инит это конструктор в классе эйайклиент
        self.provider = provider
         
        if provider == "anthropic": # ленивый импорт чтобы не загружать библиотекой ненужной
            from anthropic import Anthropic
            self._client = Anthropic()
        elif provider == "ollama":
            from openai import OpenAI
            self._client = OpenAI(
                base_url="http://localhost:11434/v1", #используем OpenAI SDK но меняем адрес на локальный. api_key="ollama" — любая строка, просто SDK требует чтобы поле не было пустым.
                api_key="ollama"
            )
    def chat(self, messages: list, system: str = "") -> str: #-> str — подсказка что метод вернёт строку
        if self.provider == "anthropic":
            response = self._client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=system,
                messages=messages
            )
            return response.content[0].text
        elif self.provider == "ollama":
            all_messages = []
            if system:
                all_messages.append({"role": "system", "content": system})
    
            for msg in messages:
                if isinstance(msg["content"], list):  # если есть картинка
                    new_content = []
                    for block in msg["content"]:
                        if block["type"] == "image":  # конвертируем формат
                            new_content.append({
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{block['source']['data']}"
                                }
                            })
                        else:
                            new_content.append(block)  # текст оставляем как есть
                    all_messages.append({"role": msg["role"], "content": new_content})
                else:
                    all_messages.append(msg)

            response = self._client.chat.completions.create(
                model="llava",
                messages=all_messages
            )
            return response.choices[0].message.content # собираем новый список: сначала system (если есть), потом остальные сообщения.