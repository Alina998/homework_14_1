from unittest import mock

import pytest

from src.main import Category, Product


# Фикстуры
@pytest.fixture
def product():
    return Product(name="Test Product", description="Test Description", price=100.0, quantity=10)


@pytest.fixture
def category(products_list):
    return Category(name="Смартфоны", description="Категория смартфонов", products=products_list)


@pytest.fixture
def products_list():
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    ]


def test_create_product(product):
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10
    assert Product.product_count == 1


def test_new_product_addition(products_list):
    new_product_data = {
        "name": "Iphone 15",
        "description": "Updated Description",
        "price": 220000.0,
        "quantity": 5
    }
    product = Product.new_product(new_product_data, products_list)

    assert product.name == "Iphone 15"
    assert product.quantity == 13  # Проверяем, что количество обновлено
    assert product.price == 220000.0  # Проверяем, что цена обновлена


def test_category_total_quantity(category):
    assert category.get_total_quantity() == 27  # 5 + 8 + 14 = 27


def test_category_add_product(category):
    new_product = Product("Google Pixel 7", "128GB, Black", 70000.0, 12)
    category.add_product(new_product)
    assert category.get_total_quantity() == 39


def test_product_price_increase(product):
    original_price = product.price
    product.price = 150.0  # Устанавливаем новую цену
    assert product.price == 150.0
    assert product.price > original_price


@mock.patch("builtins.input", side_effect=["y"])
def test_product_price_decrease_confirm(mock_input, product):
    original_price = product.price
    product.price = 50.0  # Снижаем цену с подтверждением
    assert product.price == 50.0
    assert product.price < original_price


@mock.patch("builtins.input", side_effect=["n"])
def test_product_price_decrease_cancel(mock_input, product):
    original_price = product.price
    product.price = 50.0  # Пытаемся снизить цену, но отменяем
    assert product.price == original_price  # Цена остаётся прежней


def test_product_str(product):
    assert str(product) == "Test Product, 100.0 руб. Остаток: 10 шт."


def test_category_str(category):
    assert str(category) == "Смартфоны, количество продуктов: 27 шт."


def test_products_add_operator():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    total_price = product1 + product2
    assert total_price == (180000.0 * 5 + 210000.0 * 8)


if __name__ == "__main__":
    pytest.main()
