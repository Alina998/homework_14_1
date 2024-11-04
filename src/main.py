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
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен.")
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

    def middle_price(self):
        try:
            total_price = sum(product.price*product.quantity for product in self.products)
            total_count = sum(product.quantity for product in self.products)
            return total_price / total_count
        except ZeroDivisionError:
            return 0.0


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
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
