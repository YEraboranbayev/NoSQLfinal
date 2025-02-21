import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["bike_store"]
collection = db["bikes"]

# URL каталога велосипедов
URL = "https://velopro.kz/index.php?route=common/home"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    print(" Доступ к сайту есть!")
    soup = BeautifulSoup(response.text, "html.parser")

    # Ищем карточки велосипедов (нужно проверить актуальный CSS-селектор!)
    bikes = []
    for item in soup.select(".product-thumb"):  # Проверь селектор!
        title = item.select_one(".caption a").text.strip() if item.select_one(".caption a") else "Без названия"
        price = item.select_one(".price").text.strip() if item.select_one(".price") else "Цена не указана"
        img_url = item.select_one(".image img")["src"] if item.select_one(".image img") else ""

        bike_data = {
            "title": title,
            "price": price,
            "image": img_url
        }
        
        bikes.append(bike_data)

    # Очистить старые данные и добавить новые
    collection.delete_many({})
    collection.insert_many(bikes)
    
    print(f" Успешно добавлено {len(bikes)} велосипедов в MongoDB!")
else:
    print(" Ошибка при загрузке страницы:", response.status_code)
