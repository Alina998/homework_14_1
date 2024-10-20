from unittest import mock

import pytest

from src.main import Category, Product


# Фикстуры
@pytest.fixture
def product():
    return Product(name="Test Product", description="Test Description", price=100.0, quantity=10)


@pytest.fixture
def category():
    return Category(name="Test Category", description="Test Category Description")


@pytest.fixture
def products_list():
    return [
        Product(name="Unique Product 1", description="Test Description", price=100.0, quantity=10),
        Product(name="Unique Product 2", description="Second Test Description", price=200.0, quantity=20)
    ]


def test_create_product(product):
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10
    assert Product.product_count == 1


def test_add_product_to_category(category, product):
    category.add_product(product)
    assert category.get_products() == ['Test Product, 100.0 руб. Остаток: 10 шт.']


def test_product_price_increase(product):
    original_price = product._price
    product._price = 150.0  # Устанавливаем новую цену
    assert product._price == 150.0
    assert product._price > original_price


@mock.patch("builtins.input", side_effect=["y"])
def test_product_price_decrease_confirm(mock_input, product):
    original_price = product._price
    product.price = 50.0  # Снижаем цену с подтверждением
    assert product._price == 50.0
    assert product._price < original_price


@mock.patch("builtins.input", side_effect=["n"])
def test_product_price_decrease_cancel(mock_input, product):
    original_price = product._price
    product.price = 50.0  # Пытаемся снизить цену, но отменяем
    assert product._price == original_price  # Цена остаётся прежней


@mock.patch("builtins.input", side_effect=["n"])
def test_product_price_decrease_cancel_with_greater_price(mock_input, products_list):
    product_data = {"name": "Unique Product 1", "description": "Описание товара 1", "price": 80.0, "quantity": 5}
    product = Product.new_product(product_data, products_list)
    product_data["price"] = 70.0  # Пытаемся понизить цену
    product = Product.new_product(product_data, products_list)
    assert product.price == 100.0  # Снижение цены отменяется, остаётся 100.0


if __name__ == "__main__":
    pytest.main()
