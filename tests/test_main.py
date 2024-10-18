import pytest

from src.main import Category, Product


@pytest.fixture
def product_fixture_1():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def product_fixture_2():
    return Product("Second Test Product", "Second Test Description", 200.0, 20)


@pytest.fixture
def category_fixture(product_fixture_1, product_fixture_2):
    category_1 = Category("Test Category", "Test Category Description")
    category_2 = Category("Second Test Category", "Second Test Category Description")
    category_1.add_product(product_fixture_1)
    category_2.add_product(product_fixture_2)
    return category_1, category_2


# Тестирование класса Product
def test_product_initialization(product_fixture_1, product_fixture_2):
    assert product_fixture_1.name == "Test Product"
    assert product_fixture_1.description == "Test Description"
    assert product_fixture_1.price == 100.0
    assert product_fixture_1.quantity == 10
    assert product_fixture_2.name == "Second Test Product"
    assert product_fixture_2.description == "Second Test Description"
    assert product_fixture_2.price == 200.0
    assert product_fixture_2.quantity == 20


def test_product_count_incremented():
    initial_count = Product.product_count
    _ = Product("Another Product", "Another Description", 200.0, 20)
    assert Product.product_count == initial_count + 1


# Тестирование класса Category
def test_category_initialization(category_fixture):
    category_1, category_2 = category_fixture
    assert category_1.name == "Test Category"
    assert category_1.description == "Test Category Description"
    assert category_2.name == "Second Test Category"
    assert category_2.description == "Second Test Category Description"
    assert len(category_1.products) == 1
    assert len(category_2.products) == 1


def test_category_add_product(category_fixture, product_fixture_1):
    category_1, _ = category_fixture
    assert product_fixture_1 in category_1.products


def test_category_count_incremented():
    initial_count = Category.category_count
    _ = Category("Another Category", "Another Description")
    assert Category.category_count == initial_count + 1


if __name__ == "__main__":
    pytest.main()
