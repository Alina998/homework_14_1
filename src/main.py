from abc import ABC, abstractmethod


class MixinLog:
    def __init__(self):
        print(repr(self))

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class BaseProduct(ABC):
    @abstractmethod
    def __str__(self):
        pass


# Создаем класс Product
class Product(BaseProduct, MixinLog):
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
        super().__init__()

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

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError(f"Нельзя складывать товары разных классов: {type(self).__name__}, {type(other).__name__}.")
        return self.__price * self.quantity + other.__price * other.quantity


# Создаем класс Category
class Category(Product):
    category_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products  # Присваиваем продукты из параметра

    @property
    def products(self):
        return self.__products   # Геттер для атрибута products

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError(f"Можно добавить только объекты класса Product и его наследников."
                            f"{type(product).__name__} нельзя добавить.")
        self.__products.append(product)
        Category.category_count += 1

    def __iter__(self):
        return CategoryIterator(self.__products)

    def get_total_quantity(self):
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity  # Используем атрибут quantity
        return total_quantity

    def __str__(self):
        return f"{self.name}, количество продуктов: {self.get_total_quantity()} шт."


class CategoryIterator:
    def __init__(self, products):
        self.__products = products
        self.index = 0
        self.stop = len(self.__products)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.stop:
            product = self.__products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration


class Smartphone(Product):
    efficiency: float
    model: str
    memory: int
    color = str

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return super().__str__() + f", Модель: {self.model}, Память: {self.memory} ГБ, Цвет: {self.color}"


class LawnGrass(Product):
    country: str
    germination_period: str
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return super().__str__() + f", Страна: {self.country}, Период всхожести: {self.germination_period}, Цвет: {self.color}"


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)
