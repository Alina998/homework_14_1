# Создаем класс Product
class Product:
    # Описываем атрибуты класса
    name: str
    description: str
    __price: float
    quantity: int
    product_count = 0

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        Product.product_count += 1

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value > 0:  # Проверка, чтобы цена была больше 0
            if value < self.__price:
                confirm = input("Цена снижается. Подтверждаете? (y/n): ")
                if confirm.lower() == 'y':
                    self.__price = value
                    print("Цена успешно снижена.")
                else:
                    print("Снижение цены отменено.")
            else:
                self.__price = value
        else:
            print("Цена не должна быть нулевая или отрицательная.")

    @classmethod
    def new_product(cls, product_data: dict, products_list: list):
        # Проверяем существование товара с таким же именем
        for product in products_list:
            if product.name == product_data.get("name"):
                # Обновляем количество и цену, если новая цена выше
                product.quantity += product_data.get("quantity", 0)
                if product_data.get("price", 0) > product.price:
                    product.price = product_data.get("price")
                return product

        # Если такого товара нет, создаем новый
        return cls(
            name=product_data.get("name"),
            description=product_data.get("description"),
            price=product_data.get("price"),
            quantity=product_data.get("quantity")
        )


# Создаем класс Category
class Category(Product):
    # Описываем атрибуты класса
    name: str
    description: str
    __products: list
    category_count = 0

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.__products = []

    """Функция, которая вносит в список товваров категории объекты класса Product"""

    @property
    def products(self):
        return [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products]


    def add_product(self, product: Product):
        self.__products.append(product)
        Category.category_count += 1


    # def get_products(self):
    #     return [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products]

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )

    # Добавляем продукты в категорию
    category1.add_product(product1)
    category1.add_product(product2)
    category1.add_product(product3)

    print(category1.products)
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)

    print(category1.products)
    print(Category.category_count)

    new_product = Product.new_product(
        {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
         "quantity": 5}, category1.products)   # Используем геттер для получения списка продуктов

    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    # new_product.price = 800
    # print(new_product.price)

    # new_product.price = -100
    # print(new_product.price)
    # # new_product.price = 0
    # # print(new_product.price)
