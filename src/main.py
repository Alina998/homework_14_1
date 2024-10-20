# Создаем класс Product
class Product:
    # Описываем атрибуты класса
    name: str
    description: str
    _price: float
    quantity: int
    product_count = 0

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity
        Product.product_count += 1

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif value < self._price:
            confirm = input("Цена снижается. Подтверждаете? (y/n): ")
            if confirm.lower() == 'y':
                self._price = value
                print("Цена успешно снижена.")
            else:
                print("Снижение цены отменено.")
        else:
            self._price = value

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
    category_count = 0

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

    """Функция, которая вносит в список товваров категории объекты класса Product"""
    def add_product(self, product: Product):
        self.__products.append(product)

    def get_products(self):
        return [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self.__products]
