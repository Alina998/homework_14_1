import pytest

from src.main import Category, Product


@pytest.fixture
def product_fixture():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def category_fixture(product_fixture):
    category = Category("Test Category", "Test Category Description")
    category.add_product(product_fixture)
    return category


# Тестирование класса Product
def test_product_initialization(product_fixture):
    assert product_fixture.name == "Test Product"
    assert product_fixture.description == "Test Description"
    assert product_fixture.price == 100.0
    assert product_fixture.quantity == 10


def test_product_count_incremented():
    initial_count = Product.product_count
    _ = Product("Another Product", "Another Description", 200.0, 20)
    assert Product.product_count == initial_count + 1


# Тестирование класса Category
def test_category_initialization(category_fixture):
    assert category_fixture.name == "Test Category"
    assert category_fixture.description == "Test Category Description"
    assert len(category_fixture.products) == 1


def test_category_add_product(category_fixture, product_fixture):
    assert product_fixture in category_fixture.products


def test_category_count_incremented():
    initial_count = Category.category_count
    _ = Category("Another Category", "Another Description")
    assert Category.category_count == initial_count + 1


if __name__ == "__main__":
    pytest.main()
