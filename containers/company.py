class company_class:
    def __init__(self,name):
        self.name = name 
        self.employees = {}
        self.size = 0
        
    def add(self,employee):
        self.employees[employee.name] = employee
        print(employee)
        self.size += 1
    
    def delete(self, employee):
        if employee.name in self.employees:
            removed_employee = self.employees(employee.name, None)
            self.size -= 1
            
            print(removed_employee)
            return removed_employee
    def get_employees(self):
        return self.employees
    
    def number_of_employees(self):
        return self.size
            
    

        