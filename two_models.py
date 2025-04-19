import json
from knn import load_and_prepare_data, find_nearest_neighbors_json
from lang_model import calculate_compatibility
from zone_relation import calculate_coverage
import time


def load_user_descriptions(filename):
    """Загружает только описания пользователей из JSON файла"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return {user: features.get('description', '') for user, features in data.items()}


def load_user_coords_and_time(filename, user_id):
    """
    Загружает и возвращает данные пользователя необходимые для расчета зоны проживания в структурированном виде

    Args:
        filename: Путь к JSON файлу
        user_id: ID пользователя

    Returns:
        dict: Словарь с данными вида {
            'coords': (x, y),
            'time': время,
            'other_spatial_data': ...  # при необходимости можно добавить другие поля
        } или None, если пользователь не найден
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        user_data = data.get(str(user_id))

        if not user_data:
            return None

        return {
            'coords': (user_data.get('x'), user_data.get('y')),
            'time': user_data.get('time')
        }

    except (FileNotFoundError, json.JSONDecodeError):
        return None


def find_compatible_neighbors(data_file, target_user, n=3, top_features=2, compatibility_threshold=0.65,
                              area_threshold=0.65):
    """
    Объединённая функция поиска совместимых соседей:
    1. Сначала находит ближайших соседей по числовым параметрам
    2. Затем фильтрует их по текстовой совместимости и по совпадению желаемых территорий проживания
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

        # Получаем данные о местоположении и времени
        target_data = load_user_coords_and_time(data_file, target_user)
        neighbor_data = load_user_coords_and_time(data_file, neighbor_user)

        # Проверяем, что данные существуют
        if not target_data or not neighbor_data:
            continue

        area_data = calculate_coverage(
            target_coords=target_data['coords'],
            target_time=target_data['time'],
            cand_coords=neighbor_data['coords'],
            cand_time=neighbor_data['time']
        )

        if compatibility >= compatibility_threshold and area_data >= area_threshold:
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
        target_user="user10",
        n=2,
        top_features=0,
        compatibility_threshold=0.65
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))