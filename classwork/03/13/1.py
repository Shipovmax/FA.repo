class Product:
    def __init__(self, name, manufacturer, price):
        self._name = name
        self._manufacturer = manufacturer
        self.price = price  # Вызывает сеттер для валидации

    @property
    def name(self):
        return self._name

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    def __str__(self):
        """Формальный вывод информации о товаре"""
        return f"Product: {self.name}, Manufacturer: {self.manufacturer}, Price: {self.price}"

    def matches(self, search_name=None, search_price=None):
        """Метод для проверки условий поиска"""
        if search_name and search_name.lower() in self.name.lower():
            return True
        if search_price is not None and self.price == search_price:
            return True
        return False


class Electronics(Product):
    def __init__(self, name, manufacturer, price, device_type):
        super().__init__(name, manufacturer, price)
        self._device_type = device_type

    @property
    def device_type(self):
        return self._device_type

    def __str__(self):
        return f"{super().__str__()}, Type: {self.device_type}"


class Clothing(Product):
    def __init__(self, name, manufacturer, price, size):
        super().__init__(name, manufacturer, price)
        self._size = size

    @property
    def size(self):
        return self._size

    def __str__(self):
        return f"{super().__str__()}, Size: {self.size}"


class Food(Product):
    def __init__(self, name, manufacturer, price, expiration_date):
        super().__init__(name, manufacturer, price)
        self._expiration_date = expiration_date

    @property
    def expiration_date(self):
        return self._expiration_date

    def __str__(self):
        return f"{super().__str__()}, Expires: {self.expiration_date}"



if __name__ == "__main__":
    products = [
        Electronics("iPhone 15", "Apple", 100000, "Smartphone"),
        Clothing("T-shirt", "Nike", 3000, "L"),
        Food("Milk", "Prostokvashino", 100, "14 days"),
        Electronics("Headphones", "Sony", 25000, "Audio"),
        Clothing("Jeans", "Levi's", 8000, "M"),
    ]

    print("--- Full Product List ---")
    for p in products:
        print(p)

    # Поиск по названию
    target_name = "iPhone"
    print(f"\n--- Search Results (Name: '{target_name}') ---")
    for p in products:
        if p.matches(search_name=target_name):
            print(p)

    # Поиск по цене
    target_price = 3000
    print(f"\n--- Search Results (Price: '{target_price}') ---")
    for p in products:
        if p.matches(search_price=target_price):
            print(p)
