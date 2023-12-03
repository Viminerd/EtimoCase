import http.server
import socketserver
PORT = 8080
    
from flask import Flask, jsonify, render_template, request
import json

from containers import company, employee
def create_app(test_config=None ):
    app = Flask(__name__)
    company_handler = company.company_class(name="Etimo")
    name = "TESTNAME"
    email = "TESTmsil"
    employee_to_add = employee.employee(name, email)
    company_handler.add(employee_to_add)
    #Home page
    @app.route('/')
    @describe_route("/", "[GET] Homepage for server, lists available endpoints")
    def home_page(): 
        endpoints = [
        {'endpoint': getattr(app.view_functions[rule.endpoint], '_path'), 'description': getattr(app.view_functions[rule.endpoint], '_description')}
        for rule in app.url_map.iter_rules() if rule.endpoint != 'static'
        ]
        
        return render_template('home.html', endpoints=endpoints)

    @app.route('/list_employees', methods=['GET'])
    @describe_route("/", "[GET] List of all employees")
    def employees_page(): 
        employee_list = company_handler.get_employees()
        employees = [{'name':employee.name,
        'email':employee.email}           
        for key, employee in employee_list.items()
        ]
        
        return render_template('employee_list.html', employees=employees, number = company_handler.number_of_employees())


    add_employee = "/add_employee"
    @app.route(add_employee, methods=['GET','POST'])
    @describe_route(add_employee, "[GET] Takes you to a company creation form page")
    def add_employee_form():
        if request.method == 'GET':
            print("GET")
        if request.method == 'POST':
            data = request.json
            name = data['name']
            email = data['email']
            employee_to_add = employee.employee(name, email)
            company_handler.add(employee_to_add)
        return render_template('add_employee_form.html')
    
    add_employee = "/create_company"
    @app.route(add_employee, methods=['POST'])
    @describe_route(add_employee, "[POST] Creates a new company, takes arguments (name, password)")
    def add_employee():
        return render_template('index.html')
    
    
    # create = "/create"
    # @app.route('/create/<user_id>', methods=['POST'])
    # @describe_route(create, "[POST] Creates a new company, takes arguments (name, password)")
    # def create():
    #     name = request.form
    #     print("name is : ")
    #     print(name)
    #     return render_template('index.html')
    
    
    
    
        

     
    return app

#add a rule attribute on path for hmtl display
def describe_route(path,description):
    def decorator(func):
        setattr(func, '_description', description)
        setattr(func, "_path", path)
        return func

    return decorator


APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=PORT, debug=False)
  