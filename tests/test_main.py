from unittest import mock

import pytest

from src.main import Category, LawnGrass, Product, Smartphone


# Фикстуры
@pytest.fixture
def product():
    return Product(name="Test Product", description="Test Description", price=100.0, quantity=10)


@pytest.fixture
def product_with_no_quantity():
    return Product(name="Test Product", description="Test Description", price=100.0, quantity=0)


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


@pytest.fixture
def smartphone():
    return Smartphone("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")


@pytest.fixture
def lawn_grass():
    return LawnGrass("Трава Газонная", "Для парка", 1200.0, 10, "Россия", "15-20 дней", "Зеленый")


@pytest.fixture
def category(smartphone, lawn_grass):
    return Category("Электроника", "Смартфоны и другая электронная техника", [smartphone, lawn_grass])


@pytest.fixture
def empty_category():
    # Фикстура для пустой категории
    return Category("Пустая категория", "Категория без продуктов", [])


def test_create_product(product):
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10
    assert Product.product_count == 1


def value_error_test(product_with_no_quantity):
    assert str(product_with_no_quantity) == "Товар с нулевым количеством не может быть добавлен."


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
    assert category.get_total_quantity() == 15  # 5 + 10 = 15


def test_category_add_product(category):
    new_product = Product("Google Pixel 7", "128GB, Black", 70000.0, 12)
    category.add_product(new_product)
    assert category.get_total_quantity() == 27  # 15 + 12 = 27


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
    assert str(category) == "Электроника, количество продуктов: 15 шт."


def test_products_add_operator():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    total_price = product1 + product2
    assert total_price == (180000.0 * 5 + 210000.0 * 8)


def test_smartphone_initialization(smartphone):
    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.description == "256GB"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_initialization(lawn_grass):
    assert lawn_grass.name == "Трава Газонная"
    assert lawn_grass.description == "Для парка"
    assert lawn_grass.price == 1200.0
    assert lawn_grass.quantity == 10
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "15-20 дней"
    assert lawn_grass.color == "Зеленый"


def test_category_initialization(category):
    assert category.name == "Электроника"
    assert len(category.products) == 2
    assert isinstance(category.products[0], Smartphone)
    assert isinstance(category.products[1], LawnGrass)


def test_middle_price_empty(empty_category):
    assert empty_category.middle_price() == 0.0


def test_add_product(category):
    new_smartphone = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    category.add_product(new_smartphone)
    assert len(category.products) == 3
    assert category.products[2].model == "15"


def test_add_invalid_product(category):
    with pytest.raises(TypeError):
        category.add_product("Возникла ошибка TypeError при добавлении не продукта")


def test_add_same_product_type(smartphone):
    another_smartphone = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    assert smartphone + another_smartphone == (smartphone.price * smartphone.quantity +
                                                 another_smartphone.price * another_smartphone.quantity)


def test_add_different_product_type(smartphone, lawn_grass):
    with pytest.raises(TypeError) as excinfo:
        _ = smartphone + lawn_grass
    assert str(excinfo.value) == "Нельзя складывать товары разных классов: Smartphone, LawnGrass."


if __name__ == "__main__":
    pytest.main()
