from abc import ABC, abstractmethod

# ==========================================
# 1. Abstract Base Class
# ==========================================
class Employee(ABC):
    def __init__(self, name, emp_id):
        self.name = name
        self.emp_id = emp_id

    @abstractmethod
    def calculate_pay(self):
        """Har child class ko yeh method implement karna zaroori hai."""
        pass

    def get_summary(self):
        """Payroll summary generate karne ke liye common method."""
        pay = self.calculate_pay()
        return f"ID: {self.emp_id:<5} | Name: {self.name:<10} | Role: {self.__class__.__name__:<18} | Pay: ${pay:.2f}"


# ==========================================
# 2. Child Classes (Different Pay Formulas)
# ==========================================
class SalariedEmployee(Employee):
    def __init__(self, name, emp_id, monthly_salary):
        super().__init__(name, emp_id)
        self.monthly_salary = monthly_salary

    def calculate_pay(self):
        return self.monthly_salary


class HourlyEmployee(Employee):
    def __init__(self, name, emp_id, hourly_rate, hours_worked):
        super().__init__(name, emp_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self):
        if self.hours_worked <= 40:
            return self.hours_worked * self.hourly_rate
        else:
            # 40 hours normal + overtime @ 1.5x
            regular_pay = 40 * self.hourly_rate
            overtime_pay = (self.hours_worked - 40) * (self.hourly_rate * 1.5)
            return regular_pay + overtime_pay


class CommissionEmployee(Employee):
    def __init__(self, name, emp_id, base_salary, sales, commission_rate):
        super().__init__(name, emp_id)
        self.base_salary = base_salary
        self.sales = sales
        self.commission_rate = commission_rate

    def calculate_pay(self):
        return self.base_salary + (self.sales * self.commission_rate)


# ==========================================
# 3. Unified Payroll Generator
# ==========================================
def generate_payroll(employees):
    print("-" * 75)
    print(f"{'PAYROLL SUMMARY':^75}")
    print("-" * 75)
    
    total_payroll = 0
    
    # Polymorphism: Employee list mein har object apna calculate_pay() chala raha hai
    for emp in employees:
        summary = emp.get_summary()
        print(summary)
        total_payroll += emp.calculate_pay()
        
    print("-" * 75)
    print(f"Total Payroll Amount: ${total_payroll:.2f}")
    print("-" * 75)


# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    # Test cases to verify sample behavior
    h_emp = HourlyEmployee("Ali", "E101", hourly_rate=20, hours_worked=45)
    c_emp = CommissionEmployee("Sara", "E102", base_salary=500, sales=4000, commission_rate=0.10)
    s_emp = SalariedEmployee("John", "E103", monthly_salary=3000)

    # Verify expected sample calculations directly
    print(f"Hourly Pay Expected 950 -> Got: {h_emp.calculate_pay()}")
    print(f"Commission Pay Expected 900 -> Got: {c_emp.calculate_pay()}")
    print("\n")

    # Unified Summary generate karna
    employees = [s_emp, h_emp, c_emp]
    generate_payroll(employees)

    # Test Abstract Class Instantiation (Should raise error)
    try:
        emp = Employee("Test", "E000")
    except TypeError as e:
        print(f"\n[PREVENTED] Direct Employee instantiation: {e}")