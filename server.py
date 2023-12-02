import http.server
import socketserver
PORT = 8080
    
from flask import Flask, jsonify, render_template



def create_app(test_config=None ):
    app = Flask(__name__)
    
    #Home page
    @app.route('/')
    @describe_route("/", "Homepage for server, lists available endpoints")
    def home_page(): 
        endpoints = [
        {'endpoint': getattr(app.view_functions[rule.endpoint], '_path'), 'description': getattr(app.view_functions[rule.endpoint], '_description')}
        for rule in app.url_map.iter_rules() if rule.endpoint != 'static'
        ]
        
        return render_template('index.html', endpoints=endpoints)

     
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
  