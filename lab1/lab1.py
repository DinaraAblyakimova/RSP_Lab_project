class Customer:
    def __init__(self, customer_id, last_name, first_name, patronymic, address, credit_card_number, bank_account_number):
        self.customer_id = customer_id  
        self.last_name = last_name  
        self.first_name = first_name  
        self.patronymic = patronymic  
        self.address = address  
        self.credit_card_number = credit_card_number  
        self.bank_account_number = bank_account_number  

    def set_credit_card_number(self, credit_card_number):
    
        self.credit_card_number = credit_card_number

    def get_credit_card_number(self):
    
        return self.credit_card_number

    def __str__(self):
        return (f'Customer(id={self.customer_id}, last_name={self.last_name}, first_name={self.first_name}, '
                f'patronymic={self.patronymic}, address={self.address}, '
                f'credit_card_number={self.credit_card_number}, bank_account_number={self.bank_account_number})')

    def __hash__(self):
        return hash((self.customer_id, self.credit_card_number))


def filter_customers(customers, criteria):
    return [customer for customer in customers if criteria(customer)]

def alphabetical_order_criteria():
    return lambda customer: (customer.last_name, customer.first_name, customer.patronymic)

def credit_card_range_criteria(min_card_number, max_card_number):
    return lambda customer: min_card_number <= customer.credit_card_number <= max_card_number


customers = [
    Customer(1, "Иванов", "Иван", "Иванович", "Москва, ул. Ленина, 1", 1234567890123456, "RU123456789012345678"),
    Customer(2, "Петров", "Петр", "Петрович", "Санкт-Петербург, ул. Красная, 10", 2345678901234567, "RU123456789012345679"),
    Customer(3, "Сидоров", "Сидор", "Сидорович", "Казань, ул. Зеленая, 5", 3456789012345678, "RU123456789012345680"),
    Customer(4, "Смирнов", "Сергей", "Сергеевич", "Екатеринбург, ул. Синяя, 15", 4567890123456789, "RU123456789012345681"),
    Customer(5, "Кузнецов", "Алексей", "Алексеевич", "Нижний Новгород, ул. Белая, 20", 5678901234567890, "RU123456789012345682"),
]

print("Список покупателей в алфавитном порядке:")
for customer in sorted(customers, key=alphabetical_order_criteria()):
    print(customer)


min_card = 2345678901234567
max_card = 4567890123456789
print(f"\nПокупатели с номерами кредитных карточек в диапазоне {min_card} - {max_card}:")
for customer in filter_customers(customers, credit_card_range_criteria(min_card, max_card)):
    print(customer)