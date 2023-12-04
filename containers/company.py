class company_class:
    def __init__(self,name):
        self.name = name 
        self.employees = {}
        self.size = 0
        
    def add(self,employee):
        self.employees[employee.email] = employee
        self.size += 1
    
    def delete(self, employee):
        if employee.email in self.employees:
            removed_employee = self.employees.pop(employee.email)
            self.size -= 1
            return removed_employee
        
    def get_employees(self):
        return self.employees
    
    def number_of_employees(self):
        return self.size
    
    def email_occupied(self, email):
        if email in self.employees:
            return True       
        return False 
                    
    

        