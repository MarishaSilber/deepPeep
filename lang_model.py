import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

API_KEY= os.getenv("OPENROUTE_API_KEY")  # Теперь ключ берётся из .env
MODEL = "google/gemini-pro"

def calculate_compatibility(text1: str, text2: str) -> float:
    """
    Принимает два текста, возвращает число от 0 до 1.
    """
    prompt = f"""
        Оцени совместимость этих текстов ЦИФРОЙ от 1 до 100.
        Отвечай ТОЛЬКО числом без комментариев, точек или других символов.

        Текст 1: {text1}
        Текст 2: {text2}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.05
        }
    )

    return int(response.json()['choices'][0]['message']['content'].strip()) / 100


