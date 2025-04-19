import requests
import json

# Настройки
API_KEY = "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"  # Замените на ваш реальный API-ключ OpenRouter
MODEL = "google/gemini-pro"

def calculate_compatibility(text1: str, text2: str) -> int:
    """
    Принимает два текста, возвращает ТОЛЬКО число от 1 до 100.
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
            "temperature": 0.1  # Минимизируем случайность
        }
    )

    # Извлекаем чистое число из ответа
    return int(response.json()['choices'][0]['message']['content'].strip())


