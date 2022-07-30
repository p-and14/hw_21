from abc import ABC, abstractmethod


class Storage(ABC):
    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def capacity(self):
        pass

    @abstractmethod
    def add(self, name, count):
        pass

    @abstractmethod
    def remove(self, name, count):
        pass

    @abstractmethod
    def check_item(self, name):
        pass

    @abstractmethod
    def _get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    @property
    def items(self):
        return self._items

    @property
    def capacity(self):
        return self._capacity

    def _set_capacity(self, value):
        self._capacity = value

    def add(self, name, count):
        if self._capacity > 0 and self._capacity >= count:
            if self.check_item(name):
                self.items[name] += count
            else:
                self.items[name] = count
            self._set_capacity(self._capacity - count)

            print(f"Курьер доставил {count} {name} на склад")
        else:
            raise WarehousesException("На складе недостаточно места")

    def remove(self, name, count):
        if self.check_item(name):
            if self._items[name] >= count:
                print("\nНужное количество есть на складе")
                self._items[name] -= count
                self._set_capacity(self._capacity + count)
                print(f"Курьер забрал {count} {name} со склада")
                if self._items[name] == 0:
                    self._items.pop(name)
            else:
                raise WarehousesException("Не хватает на складе, попробуйте заказать меньше")
        else:
            raise WarehousesException("На складе нет такого товара, попробуйте заказать что-то другое")

    def check_item(self, name):
        return name in self._items

    def _get_unique_items_count(self):
        return len(self.items.keys())


class Shop(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 20
        self._unique_items_count = 5

    @property
    def items(self):
        return self._items

    @property
    def capacity(self):
        return self._capacity

    def _set_capacity(self, value):
        self._capacity = value

    def add(self, name, count):
        if self._capacity > 0 and self._capacity >= count:
            if self.check_item(name) and self._get_unique_items_count() <= self._unique_items_count:
                self.items[name] += count
                self._set_capacity(self._capacity - count)
                print(f"Курьер доставил {count} {name} в магазин")
            elif self._get_unique_items_count() < self._unique_items_count:
                self.items[name] = count
                self._set_capacity(self._capacity - count)
                print(f"Курьер доставил {count} {name} в магазин")
            else:
                raise WarehousesException("В магазине недостаточно места")
        else:
            raise WarehousesException("В магазине недостаточно места")

    def remove(self, name, count):
        if self.check_item(name):
            if self._items[name] >= count:
                print("\nНужное количество есть в магазине")
                self._items[name] -= count
                self._set_capacity(self._capacity + count)
                print(f"Курьер забрал {count} {name} из магазина")

                if self._items[name] == 0:
                    self._items.pop(name)
            else:
                raise WarehousesException("Не хватает в магазине, попробуйте заказать меньше")
        else:
            raise WarehousesException("В магазине нет такого товара, попробуйте заказать что-то другое")

    def check_item(self, name):
        return name in self._items

    def _get_unique_items_count(self):
        return len(self.items.keys())


class Request:
    def __init__(self, warehouse_list, request: str):
        self.request_list = request.split(" ")
        self.from_ = self.request_list[-3]
        self.to = self.request_list[-1]
        if all(x in warehouse_list for x in [self.from_, self.to]):
            self.amount = int(self.request_list[-6])
            self.product = self.request_list[-5]
            self.warehouse_list = warehouse_list
        else:
            raise WarehousesException(f"Таких складов не существует: {self.from_}, {self.to}")


class WarehousesException(Exception):
    pass


def fill_with_goods(store, shop):
    store.add('собачки', 3)
    store.add('кошки', 20)
    store.add('печеньки', 20)
    store.add('коробки', 20)
    store.add('мячи', 20)

    shop.add('кошки', 2)
    shop.add('печеньки', 5)
    shop.add('коробки', 5)
    shop.add('мячи', 2)
    shop.add('собачки', 1)
    print("=" * 30, "\n")


def delivery(from_, to, request):
    from_.remove(request.product, request.amount)
    print(f"Курьер везет {request.amount} {request.product} с {request.from_} в {request.to}")
    to.add(request.product, request.amount)


def show_status(store, shop):
    print("\nВ склад хранится:")
    for name, count in store.items.items():
        print(count, name)

    print("\nВ магазин хранится:")
    for name, count in shop.items.items():
        print(count, name)


def main():
    store = Store()
    shop = Shop()
    fill_with_goods(store, shop)

    try:
        warehouse_list = ["склад", "магазин", "пункт доставки"]
        user_input = input("Введите, что необходимо доставить: ")
        request = Request(warehouse_list, user_input)

        if request.from_.lower() == "склад":
            delivery(store, shop, request)
        elif request.from_.lower() == "магазин":
            delivery(shop, store, request)

    except WarehousesException as e:
        print(e.args[0])

    show_status(store, shop)


if __name__ == "__main__":
    main()
