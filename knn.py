import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict


def load_and_prepare_data(filename):
    """Загружает JSON и преобразует в формат {user: vector}, игнорируя текстовые поля"""
    with open(filename, 'r') as f:
        raw_data = json.load(f)

    # Определяем числовые признаки (исключаем нечисловые поля как 'description')
    first_user_features = next(iter(raw_data.values()))
    feature_names = sorted(
        key for key, value in first_user_features.items()
        if isinstance(value, (int, float))
    )

    user_vectors = {}
    for user, features in raw_data.items():
        user_vectors[user] = np.array([features[feature] for feature in feature_names])

    return user_vectors, feature_names


def find_nearest_neighbors_json(data, feature_names, target_user, n=3, top_features=2):
    """
    Возвращает JSON с результатами поиска соседей (только по числовым признакам)
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

    feature_counter = defaultdict(int)
    feature_contrib_sum = defaultdict(float)
    neighbors_temp = []

    for user, vector in data.items():
        if user == target_user:
            continue

        sim = cosine_similarity([target_vector], [vector])[0][0]

        contributions = []
        for i, feature in enumerate(feature_names):
            contribution = (target_vector[i] * vector[i]) / (np.linalg.norm(target_vector) * np.linalg.norm(vector))
            contributions.append((feature, contribution))
            feature_contrib_sum[feature] += abs(contribution)

        sorted_contrib = sorted(contributions, key=lambda x: abs(x[1]), reverse=True)
        top_contrib = [{"feature": f, "contribution": round(c, 4)}
                       for f, c in sorted_contrib[:top_features]]

        for f, _ in sorted_contrib[:top_features]:
            feature_counter[f] += 1

        neighbors_temp.append({
            "user": user,
            "similarity": round(sim, 4),
            "top_features": top_contrib
        })

    neighbors_sorted = sorted(neighbors_temp, key=lambda x: x["similarity"], reverse=True)[:n]
    results["neighbors"] = neighbors_sorted

    total_pairs = len(neighbors_temp)
    if total_pairs > 0:
        common_features = sorted(feature_counter.items(), key=lambda x: x[1], reverse=True)
        results["feature_importances"]["most_common_features"] = [f[0] for f in common_features[:3]]

        for feature in feature_names:
            results["feature_importances"]["global_contributions"][feature] = round(
                feature_contrib_sum[feature] / total_pairs, 4)

    return results