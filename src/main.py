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


class LawnGrass(Product):
    country: str
    germination_period: str
    color: str

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


if __name__ == '__main__':

    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                         "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)

    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)

    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)

    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)

    smartphone_sum = smartphone1 + smartphone2
    print(smartphone_sum)

    grass_sum = grass1 + grass2
    print(grass_sum)

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")

    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    category_smartphones.add_product(smartphone3)

    print(category_smartphones.products)

    print(Category.product_count)

    try:
        category_smartphones.add_product("Not a product")
    except TypeError:
        print("Возникла ошибка TypeError при добавлении не продукта")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта")
