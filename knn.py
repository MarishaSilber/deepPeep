import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def find_nearest_neighbors(data, target_user, n=3):
    if target_user not in data:
        return None

    similarities = {}
    target_vector = np.array(data[target_user]).reshape(1, -1)

    for user, vector in data.items():
        if user == target_user:
            continue

        current_vector = np.array(vector).reshape(1, -1)
        sim = cosine_similarity(target_vector, current_vector)[0][0]
        similarities[user] = sim

    # Сортируем по убыванию сходства и возвращаем топ-N
    return sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:n]


# Пример использования
data = load_data('users.json')
target_user = "user1"
neighbors = find_nearest_neighbors(data, target_user, n=2)

print(f"Ближайшие соседи к {target_user}: {neighbors}")























