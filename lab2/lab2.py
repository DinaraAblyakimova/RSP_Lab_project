from abc import ABC, abstractmethod

class Sweet(ABC):

    def __init__(self, name: str, weight_grams: int, sugar_per_100g: int):
        self._name = name
        self._weight_grams = weight_grams
        self._sugar_per_100g = sugar_per_100g

    @property
    def name(self): return self._name

    @property
    def weight_grams(self): return self._weight_grams

    @property
    def sugar_per_100g(self): return self._sugar_per_100g

    def estimate_sugar_in_piece(self):
        return (self._weight_grams * self._sugar_per_100g) // 100

    @abstractmethod
    def kind(self): ...

    def __str__(self):
        return f"{self._name} [{self.kind()}]: weight={self._weight_grams}g, sugar={self._sugar_per_100g}g/100g"


class Candy(Sweet, ABC):

    pass


class ChocolateCandy(Candy):
    def __init__(self, name, weight, sugar, cocoa_percent, with_nuts):
        super().__init__(name, weight, sugar)
        self._cocoa_percent = cocoa_percent
        self._with_nuts = with_nuts

    def kind(self): return "Chocolate"

    def __str__(self):
        return f"{super().__str__()}, cocoa={self._cocoa_percent}%, nuts={'yes' if self._with_nuts else 'no'}"


class CaramelCandy(Candy):
    def __init__(self, name, weight, sugar, filling_flavor, hardness):
        super().__init__(name, weight, sugar)
        self._filling_flavor = filling_flavor
        self._hardness = hardness

    def kind(self): return "Caramel"

    def __str__(self):
        return f"{super().__str__()}, flavor={self._filling_flavor}, hardness={self._hardness}"


class JellyCandy(Candy):
    def __init__(self, name, weight, sugar, fruit_juice_percent, gelling_agent):
        super().__init__(name, weight, sugar)
        self._fruit_juice_percent = fruit_juice_percent
        self._gelling_agent = gelling_agent

    def kind(self): return "Jelly"

    def __str__(self):
        return f"{super().__str__()}, fruitJuice={self._fruit_juice_percent}%, agent={self._gelling_agent}"


class Cookie(Sweet):
    def __init__(self, name, weight, sugar, gluten_free):
        super().__init__(name, weight, sugar)
        self._gluten_free = gluten_free

    def kind(self): return "Cookie"

    def __str__(self):
        return f"{super().__str__()}, glutenFree={'yes' if self._gluten_free else 'no'}"



class Gift:
    def __init__(self):
        self._sweets = []

    def add(self, sweet: Sweet):
        self._sweets.append(sweet)

    def sweets(self): return list(self._sweets)

    def total_weight(self): return sum(s.weight_grams for s in self._sweets)

    def sort_by(self, key_func): self._sweets.sort(key=key_func)

    def find_by_sugar_range(self, min_val, max_val):
        return [s for s in self._sweets if min_val <= s.sugar_per_100g <= max_val]



def by_name(s): return s.name.lower()
def by_weight(s): return s.weight_grams
def by_sugar_per_100g(s): return s.sugar_per_100g
def by_estimated_sugar_in_piece(s): return s.estimate_sugar_in_piece()



def print_sweets(gift):
    if not gift.sweets():
        print("Подарок пуст.")
        return
    for i, s in enumerate(gift.sweets(), start=1):
        print(f"{i}) {s} | sugar in piece ≈ {s.estimate_sugar_in_piece()}g")


def menu():
    gift = Gift()
    gift.add(ChocolateCandy("Alpen Gold Dark", 90, 48, 70, True))
    gift.add(CaramelCandy("Barbaris Soft", 15, 65, "barberry", "SOFT"))
    gift.add(JellyCandy("Fruit Delight", 20, 60, 30, "PECTIN"))
    gift.add(Cookie("Shortbread Mini", 25, 35, True))
    gift.add(ChocolateCandy("Roasted Nuts", 25, 50, 55, True))
    gift.add(CaramelCandy("Golden Caramel", 18, 70, "classic", "HARD"))

    print(f"Загружено {len(gift.sweets())} позиций, вес = {gift.total_weight()} г")

    while True:
        print("\nМеню:")
        print("1) Показать сладости")
        print("2) Общий вес подарка")
        print("3) Сортировать")
        print("4) Найти по сахару")
        print("0) Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            print_sweets(gift)
        elif choice == "2":
            print(f"Общий вес: {gift.total_weight()} г")
        elif choice == "3":
            sort_options = {
                "1": ("названию", by_name),
                "2": ("весу", by_weight),
                "3": ("сахару (г/100г)", by_sugar_per_100g),
                "4": ("сахару в штуке", by_estimated_sugar_in_piece),
            }
            print("1) Названию\n2) Весу\n3) Сахару (г/100г)\n4) Сахару в штуке")
            c = input("Выбор: ").strip()
            if c in sort_options:
                text, func = sort_options[c]
                gift.sort_by(func)
                print(f"Отсортировано по {text}:")
                print_sweets(gift)
            else:
                print("Неверный выбор сортировки.")
        elif choice == "4":
            try:
                min_v = int(input("Мин (г/100г): "))
                max_v = int(input("Макс (г/100г): "))
                found = gift.find_by_sugar_range(min_v, max_v)
                if not found:
                    print("Ничего не найдено.")
                else:
                    for i, s in enumerate(found, start=1):
                        print(f"{i}) {s}")
            except ValueError:
                print("Ошибка ввода.")
        elif choice == "0":
            print("Пока!")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    print("=== Новогодний подарок ===")
    menu()
