import requests

class LLMService:
    
    # Параметры запроса к LLM
    api_url: str = "http://127.0.0.1:1234/v1/chat/completions"
    model: str = "qwen3-vl-30b"
    temperature = 0.5
    max_tokens = -1
    system_prompt_content: str = "Ты - медицинский ассистент. На основе диалога врача и пациента сформируй JSON с полями: " \
                                 "complaints, anamnesis, status_praesens, recommendations"

    # Метод класса для отправки промпта и получения ответа
    @classmethod
    def send_message(cls, message: str) -> dict:
        headers = {'Content-Type': 'application/json'}
        data = {
            "model": cls.model,
            "messages": [
                {"role": "system", "content": cls.system_prompt_content},
                {"role": "user", "content": message}                               
            ],
            "temperature": cls.temperature,
            "max_tokens": cls.max_tokens,
            "stream": False
        }
        response = requests.post(cls.api_url, json=data, headers=headers)
        raw = response.json()

        return raw['choices'][0]['message']['content']