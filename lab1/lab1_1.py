class Abiturient:
    def __init__(self, Surname = "Не указано", Name = "Не указано", Fathername = "Не указано", Adress = "Не указано", Grades = "Не указано"):
        self.surname = Surname
        self.name = Name
        self.fathername = Fathername
        self.adress = Adress
        self.grades = Grades
    

    def display_info(self):
        print(f"Фамилия: {self.surname}, Имя: {self.name}, Отчество: {self.fathername}")
        print(f"Адрес: {self.adress}")
        print(f"Оценки: {self.grades}")

abiturient1 = Abiturient("Аблякимовва", "Динара", "Наримановна", "г. Судак", [5, 4, 3, 5, 4])
abiturient1.display_info()
abiturient2 = Abiturient()
abiturient2.display_info()