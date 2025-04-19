import json
from knn import load_and_prepare_data, find_nearest_neighbors_json
from lang_model import calculate_compatibility


def load_user_descriptions(filename):
    """Загружает только описания пользователей из JSON файла"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return {user: features.get('description', '') for user, features in data.items()}


def find_compatible_neighbors(data_file, target_user, n=3, top_features=2, compatibility_threshold=0.65):
    """
    Объединённая функция поиска совместимых соседей:
    1. Сначала находит ближайших соседей по числовым параметрам
    2. Затем фильтрует их по текстовой совместимости
    """
    # Загружаем данные
    user_vectors, feature_names = load_and_prepare_data(data_file)
    user_descriptions = load_user_descriptions(data_file)

    if target_user not in user_vectors:
        return {"error": f"User {target_user} not found in data"}

    # Шаг 1: Поиск ближайших соседей по числовым параметрам
    knn_results = find_nearest_neighbors_json(
        user_vectors,
        feature_names,
        target_user,
        n=n * 3,  # Берем больше соседей для запаса
        top_features=top_features
    )

    if "error" in knn_results:
        return knn_results

    # Шаг 2: Фильтрация по совместимости описаний
    target_description = user_descriptions.get(target_user, '')
    compatible_neighbors = []

    for neighbor in knn_results["neighbors"]:
        neighbor_user = neighbor["user"]
        neighbor_description = user_descriptions.get(neighbor_user, '')

        compatibility = calculate_compatibility(target_description, neighbor_description)
        if compatibility >= compatibility_threshold:
            neighbor_with_compat = neighbor.copy()
            neighbor_with_compat["compatibility"] = round(compatibility, 4)
            compatible_neighbors.append(neighbor_with_compat)

            if len(compatible_neighbors) >= n:
                break

    # Формируем итоговый результат
    result = {
        "target_user": target_user,
        "compatibility_threshold": compatibility_threshold,
        "initial_neighbors_count": len(knn_results["neighbors"]),
        "compatible_neighbors": compatible_neighbors,
        "feature_importances": knn_results["feature_importances"]
    }

    return result


if __name__ == "__main__":
    result = find_compatible_neighbors(
        data_file='users.json',
        target_user="user4",
        n=4,
        top_features=1,
        compatibility_threshold=0.65
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))