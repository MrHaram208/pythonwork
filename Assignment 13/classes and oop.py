# Q1.
class Student:
    def __init__(self, name, marks=0):
        self.name = name
        self._marks = 0
        self.__grade = "F"
        self.set_marks(marks)

    def set_marks(self, marks):
        if 0 <= marks <= 100:
            self._marks = marks
            if marks >= 80:
                self.__grade = "A"
            elif marks >= 60:
                self.__grade = "B"
            elif marks >= 40:
                self.__grade = "C"
            else:
                self.__grade = "F"
        else:
            print("Error: Marks must be between 0 and 100.")

    def get_marks(self):
        return self._marks

    def get_grade(self):
        return self.__grade

print("--- Q1 Output ---")
s1 = Student("Ali", 85)
print("Student 1:", s1.name, s1.get_marks(), s1.get_grade())
s1.set_marks(105)
print("Student 1 after invalid:", s1.get_marks())
s2 = Student("Sara", 55)
print("Student 2:", s2.name, s2.get_marks(), s2.get_grade())
print("\n")


# Q2.
class BankAccount:
    def __init__(self, name, balance, pin):
        self.name = name
        self.__balance = balance
        self.__pin = pin

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Deposited:", amount)
        else:
            print("Error: Deposit must be positive.")

    def withdraw(self, amount, pin):
        if pin != self.__pin:
            print("Error: Incorrect PIN.")
        elif amount <= 0:
            print("Error: Withdrawal must be positive.")
        elif amount > self.__balance:
            print("Error: Insufficient balance.")
        else:
            self.__balance -= amount
            print("Withdrawn:", amount)

    def get_balance(self, pin):
        if pin == self.__pin:
            return self.__balance
        else:
            print("Error: Incorrect PIN.")

print("--- Q2 Output ---")
acc1 = BankAccount("Ali", 5000, 1234)
acc1.deposit(2000)
acc1.withdraw(1000, 1234)
acc1.withdraw(10000, 1234)
acc1.withdraw(500, 1111)
print("Balance:", acc1.get_balance(1234))
print("\n")



# Q3.
class Employee:
    def __init__(self, name, emp_id):
        self.name = name
        self.emp_id = emp_id

    def display_details(self):
        print("Name:", self.name, "| ID:", self.emp_id)

class Developer(Employee):
    def __init__(self, name, emp_id, language):
        super().__init__(name, emp_id)
        self.language = language

    def display_details(self):
        super().display_details()
        print("Role: Developer | Language:", self.language)

class Manager(Employee):
    def __init__(self, name, emp_id, team_size):
        super().__init__(name, emp_id)
        self.team_size = team_size

    def display_details(self):
        super().display_details()
        print("Role: Manager | Team Size:", self.team_size)

print("--- Q3 Output ---")
dev = Developer("Ali", "D01", "Python")
mgr = Manager("Sara", "M01", 5)
dev.display_details()
print("---")
mgr.display_details()
print("\n")



# Q4. 
class Vehicle:
    def __init__(self, brand, model, daily_rate):
        self.brand = brand
        self.model = model
        self.daily_rate = daily_rate

    def calculate_rent(self, days):
        if days <= 0:
            print("Error: Days must be greater than 0.")
            return 0
        return self.daily_rate * days

class Car(Vehicle):
    def calculate_rent(self, days):
        base = super().calculate_rent(days)
        if base > 0:
            return base + 1000
        return 0

class Bike(Vehicle):
    def calculate_rent(self, days):
        base = super().calculate_rent(days)
        if base > 0:
            return base - (base * 0.10)
        return 0

print("--- Q4 Output ---")
car = Car("Toyota", "Corolla", 5000)
bike = Bike("Honda", "CD70", 2000)
print("Car Rent:", car.calculate_rent(3))
print("Bike Rent:", bike.calculate_rent(3))
print("Car Rent (invalid):", car.calculate_rent(0))
print("\n")


# Q5. 
class EmailNotification:
    def send(self, message):
        print("Email sent:", message)

class SMSNotification:
    def send(self, message):
        print("SMS sent:", message)

class PushNotification:
    def send(self, message):
        print("Push sent:", message)

class WhatsAppNotification:
    def send(self, message):
        print("WhatsApp sent:", message)

def notify_all(notifications, message):
    for n in notifications:
        n.send(message)

print("--- Q5 Output ---")
notify_all([EmailNotification(), SMSNotification(), PushNotification()], "Welcome!")
notify_all(WhatsAppNotification(), "Hello!")
print("\n")


# Q6. 
class RegularCustomer:
    def final_price(self, amount):
        if amount < 0:
            print("Error: Negative amount.")
            return 0
        return amount - (amount * 0.05)

class PremiumCustomer:
    def final_price(self, amount):
        if amount < 0:
            print("Error: Negative amount.")
            return 0
        return amount - (amount * 0.10)

class VIPCustomer:
    def final_price(self, amount):
        if amount < 0:
            print("Error: Negative amount.")
            return 0
        return amount - (amount * 0.20)

class GoldCustomer:
    def final_price(self, amount):
        if amount < 0:
            print("Error: Negative amount.")
            return 0
        return amount - (amount * 0.15)

def print_receipt(customer, amount):
    print("Final Price:", customer.final_price(amount))

print("--- Q6 Output ---")
print_receipt(RegularCustomer(), 10000)
print_receipt(PremiumCustomer(), 10000)
print_receipt(VIPCustomer(), 10000)
print_receipt(GoldCustomer(), 10000)
print_receipt(RegularCustomer(), -500)
print("\n")


# Q7.
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

print("--- Q7 Output ---")
c = Circle(5)
r = Rectangle(4, 6)
print("Circle Area:", c.area(), "Perimeter:", c.perimeter())
print("Rectangle Area:", r.area(), "Perimeter:", r.perimeter())
print("\n")



# Q8.
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

class CardPayment(PaymentMethod):
    def pay(self, amount):
        if amount > 0:
            print(f"Card Payment: Paid Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

    def refund(self, amount):
        if amount > 0:
            print(f"Card Payment: Refunded Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

class WalletPayment(PaymentMethod):
    def pay(self, amount):
        if amount > 0:
            print(f"Wallet Payment: Paid Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

    def refund(self, amount):
        if amount > 0:
            print(f"Wallet Payment: Refunded Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

class BankTransferPayment(PaymentMethod):
    def pay(self, amount):
        if amount > 0:
            print(f"Bank Transfer: Paid Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

    def refund(self, amount):
        if amount > 0:
            print(f"Bank Transfer: Refunded Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

class CryptoPayment(PaymentMethod):
    def pay(self, amount):
        if amount > 0:
            print(f"Crypto Payment: Paid Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

    def refund(self, amount):
        if amount > 0:
            print(f"Crypto Payment: Refunded Rs. {amount}")
        else:
            print("Error: Amount must be positive.")

def process_transaction(method, amount):
    method.pay(amount)

def process_refund(method, amount):
    method.refund(amount)

print("--- Q8 Output ---")
process_transaction(CardPayment(), 5000)
process_transaction(WalletPayment(), 2000)
process_transaction(BankTransferPayment(), 10000)
process_transaction(CryptoPayment(), 15000)
process_refund(CardPayment(), 1000)
