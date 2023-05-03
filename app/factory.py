from flask import Flask
from app.api.employeeimport import employeeimport

def create_app():
    app = Flask(__name__)
    app.register_blueprint(employeeimport, url_prefix=employeeimport.url_prefix)

    return app