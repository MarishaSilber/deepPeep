import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict, defaultdict


def load_and_prepare_data(filename):
    """Загружает JSON и преобразует в формат {user: vector}"""
    with open(filename, 'r') as f:
        raw_data = json.load(f)

    feature_names = sorted(next(iter(raw_data.values())).keys())
    user_vectors = {}

    for user, features in raw_data.items():
        user_vectors[user] = np.array([features[feature] for feature in feature_names])

    return user_vectors, feature_names


def find_nearest_neighbors_json(data, feature_names, target_user, n=3, top_features=2):
    """
    Возвращает JSON с результатами поиска соседей
    Формат возврата:
    {
        "target_user": "user1",
        "neighbors": [
            {
                "user": "user3",
                "similarity": 0.942,
                "top_features": [
                    {"feature": "price_sensitivity", "contribution": 0.512},
                    {"feature": "room_size_pref", "contribution": 0.378}
                ]
            },
            ...
        ],
        "feature_importances": {
            "most_common_features": ["price_sensitivity", "room_size_pref"],
            "global_contributions": {
                "price_sensitivity": 0.45,
                "room_size_pref": 0.32,
                ...
            }
        }
    }
    """
    if target_user not in data:
        return {"error": f"User {target_user} not found in data"}

    target_vector = data[target_user]
    results = {
        "target_user": target_user,
        "neighbors": [],
        "feature_importances": {
            "most_common_features": [],
            "global_contributions": {feature: 0.0 for feature in feature_names}
        }
    }

    # Собираем статистику по всем признакам
    feature_counter = defaultdict(int)
    feature_contrib_sum = defaultdict(float)

    # Временное хранилище для соседей
    neighbors_temp = []

    for user, vector in data.items():
        if user == target_user:
            continue

        # Вычисляем сходство
        sim = cosine_similarity([target_vector], [vector])[0][0]

        # Анализируем вклад признаков
        contributions = []
        for i, feature in enumerate(feature_names):
            contribution = (target_vector[i] * vector[i]) / (np.linalg.norm(target_vector) * np.linalg.norm(vector))
            contributions.append((feature, contribution))
            feature_contrib_sum[feature] += abs(contribution)  # Используем модуль для общей значимости

        # Сортируем признаки по абсолютному вкладу
        sorted_contrib = sorted(contributions, key=lambda x: abs(x[1]), reverse=True)

        # Записываем топовые признаки
        top_contrib = [{"feature": f, "contribution": round(c, 4)}
                       for f, c in sorted_contrib[:top_features]]

        # Обновляем счетчики важных признаков
        for f, _ in sorted_contrib[:top_features]:
            feature_counter[f] += 1

        neighbors_temp.append({
            "user": user,
            "similarity": round(sim, 4),
            "top_features": top_contrib
        })

    # Сортируем соседей по сходству
    neighbors_sorted = sorted(neighbors_temp, key=lambda x: x["similarity"], reverse=True)[:n]
    results["neighbors"] = neighbors_sorted

    # Анализ общей важности признаков
    total_pairs = len(neighbors_temp)
    if total_pairs > 0:
        # Самые часто встречающиеся в топах признаки
        common_features = sorted(feature_counter.items(), key=lambda x: x[1], reverse=True)
        results["feature_importances"]["most_common_features"] = [f[0] for f in common_features[:3]]

        # Средний вклад признаков
        for feature in feature_names:
            results["feature_importances"]["global_contributions"][feature] = round(
                feature_contrib_sum[feature] / total_pairs, 4)

    return results


# Пример использования
if __name__ == "__main__":
    # Загрузка данных
    user_vectors, feature_names = load_and_prepare_data('users.json')

    # Поиск соседей с выводом в JSON
    result_json = find_nearest_neighbors_json(
        user_vectors,
        feature_names,
        target_user="user1",
        n=2,
        top_features=1
    )

    # Красивый вывод JSON
    print(json.dumps(result_json, indent=2, ensure_ascii=False))