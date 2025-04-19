import requests
import json
import re
import time


def get_compatibility_score(text1: str, text2: str) -> int:
    """
    Анализирует совместимость двух людей и возвращает число от 1 до 100.
    Молча пытается 3 раза, возвращает 50 если не получилось.

    :param text1: Текст первого человека
    :param text2: Текст второго человека
    :return: Оценка совместимости (1-100), 50 по умолчанию
    """
    OPENROUTER_API_KEY = "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"
    MODEL = "google/gemini-pro"

    prompt = f"""ТОЛЬКО ОДНО ЧИСЛО ОТ 1 ДО 100, НИЧЕГО БОЛЬШЕ!
Оцени совместимость для сожительства на основе:
"{text1}"
"{text2}"
Только число:"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "Compatibility Checker"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,  # Минимальная креативность
        "max_tokens": 5,  # Жесткое ограничение длины
    }

    for _ in range(3):  # 3 молчаливые попытки
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=5
            )
            response.raise_for_status()

            content = response.json()["choices"][0]["message"]["content"].strip()
            match = re.search(r'^\s*(\d{1,3})\s*$', content)  # Только число

            if match:
                score = int(match.group(1))
                if 1 <= score <= 100:
                    return score

        except:
            pass  # Полностью подавляем ошибки

        time.sleep(0.5)  # Короткая пауза между попытками

    return 50  # Значение по умолчанию

a = time.time()
for i in range(2):
    text1 = "Я люблю порядок и тишину."
    text2 = "ненавижу спонтанность и вечеринки!"
    score = get_compatibility_score(text1, text2)
    print(score / 100)  # Выведет только число, например: 42
print(time.time() - a)