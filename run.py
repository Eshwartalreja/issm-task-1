
from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from utils.db_utils import init_db
from routes.book_routes import book_bp
from routes.customer_routes import customer_bp
from routes.supplier_routes import supplier_bp
from routes.employee_routes import employee_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

init_db(app)

app.register_blueprint(book_bp, url_prefix='/api/books')
app.register_blueprint(customer_bp, url_prefix='/api/customers')
app.register_blueprint(employee_bp, url_prefix='/api/employees')
app.register_blueprint(supplier_bp, url_prefix='/api/suppliers')

if __name__ == '__main__':
    app.run(port=4000,debug=True)