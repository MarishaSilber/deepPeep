import openrouteservice
from openrouteservice import convert
import folium

# 🔑 Вставь свой API-ключ сюда
api_key = "5b3ce3597851110001cf6248380fc6366e2248ecb87916d4ee5662d8"

client = openrouteservice.Client(key=api_key)

# 🗺️ Пример: МГУ
location = (37.5302, 55.7033)  # (lon, lat)

# 🕐 Время в минутах (в миллисекундах)
travel_time = 35 * 60  # 15 минут

# 🚶 Тип перемещения: foot-walking, driving-car, cycling-regular
params = {
    'locations': [location],
    'profile': 'foot-walking',
    'range': [travel_time],
    'units': 'm',
    'location_type': 'start',
    'interval': travel_time
}

iso = client.isochrones(**params)

# 🌍 Отображение на карте
m = folium.Map(location=[location[1], location[0]], zoom_start=14)

folium.GeoJson(iso, style_function=lambda x: {
    'fillColor': '#007AFF',
    'color': '#007AFF',
    'fillOpacity': 0.3
}).add_to(m)

folium.Marker(
    location=[location[1], location[0]],
    popup='Start Point',
    icon=folium.Icon(color='blue')
).add_to(m)

# 💾 Сохраняем карту
m.save("isochrone_map.html")
print("Карта сохранена как isochrone_map.html")


