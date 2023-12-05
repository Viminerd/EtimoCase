class company_class:
    def __init__(self,name):
        self.name = name 
        self.employees = {}
        self.size = 0
        
    def add(self,employee):
        if employee.email not in self.employees:
            employee.email = employee.email.lower()
            self.employees[employee.email] = employee
            self.size += 1
            return True
        else:
            return False
    
    def delete(self, employee):
        if employee.email in self.employees:
            removed_employee = self.employees.pop(employee.email)
            self.size -= 1
            return True
        else:
            return False
        
    def get_employees(self):
        return self.employees
    
    def number_of_employees(self):
        return self.size
    
    def email_occupied(self, email):
        if email in self.employees:
            return True       
        return False 
    
    def reset(self, reset_passsword):
        if (reset_passsword == "Admin_password"):
            self.employees.clear()
            self.size=0
            return True
        return False
                    
    

        