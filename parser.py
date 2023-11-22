import requests
from pathlib import Path
import csv


def get_data(store_id: int, slug: str) -> dict:
    url = 'https://api.metro-cc.ru/products-api/graph'
    query = {
        "query": "query Query($storeId: Int!, $slug: String!, $from: Int!, $size: Int!, $inStock: Boolean, $eshopAvailability: Boolean) {\n  category(storeId: $storeId, slug: $slug, inStock: $inStock, eshopAvailability: $eshopAvailability) {\n    products(from: $from, size: $size) {\n      id\n      name\n      url\n      stocks {\n        prices {\n          price\n          old_price\n        }\n      }\n      attributes {\n        name\n        text\n      }\n    }\n  }\n}\n",
        "variables": {
            "storeId": store_id,
            "slug": slug,
            "from": 0,
            "size": 1000,
            "inStock": True,  # показывает, что товар в наличии
            "eshopAvailability": True  # показывает, что товар можно заказать онлайн
        },
        "operationName": "Query"
    }
    headers = {'Content-Type': 'application/json'}

    return requests.post(url, json=query, headers=headers).json()


def write_data(data: dict, file_path: Path) -> None:
    with open(file_path, 'w+', newline='') as file:
        writer = csv.writer(file)

        columns = ['id товара из сайта', 'наименование', 'ссылка на товар', 'регулярная цена', 'промо цена', 'бренд']
        writer.writerow(columns)

        for product in data['data']['category']['products']:
            product_id = product['id']
            product_name = product['name']
            product_url = 'https://online.metro-cc.ru' + product['url']
            product_price = product['stocks'][0]['prices']['price']
            product_old_price = product['stocks'][0]['prices']['old_price']
            if product_old_price is not None:
                product_price, product_old_price = product_old_price, product_price
            brand = product['attributes'][0]['text']

            writer.writerow([product_id, product_name, product_url, product_price, product_old_price, brand])


if __name__ == '__main__':
    target_store_id = 10  # по API METRO это магазин по адресу Москва, Ленинградское ш., д.71Г
    target_category = 'sladosti-chipsy-sneki'  # название категории, по которой парсим
    target_file = Path('results.csv')

    response = get_data(target_store_id, target_category)
    write_data(response, target_file)
