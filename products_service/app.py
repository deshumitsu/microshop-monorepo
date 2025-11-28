# Микросервис управления товарами

import os
import yaml
from flask import Flask, jsonify

app = Flask(__name__)

def load_products():
    """Загружает список товаров из products.yaml"""
    yaml_path = os.path.join(os.path.dirname(__file__), "products.yaml")

    try:
        with open(yaml_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
            return data.get("items", [])
    except FileNotFoundError:
        print("Файл products.yaml не найден")
        return []
    except yaml.YAMLError as e:
        print(f"Ошибка в синтаксисе YAML: {e}")
        return []

products = load_products()

@app.route('/products', methods=['GET'])
def get_products():
    """Получить список всех товаров"""
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить товар по ID"""
    product = next((prod for prod in products if prod.get("id") == product_id), None)
    return jsonify(product) if product else ('Not Found', 404)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
