
from utils.db_utils import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    

     
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='SET NULL'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', ondelete='SET NULL'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='SET NULL'), nullable=True)

    
    customer = db.relationship('Customer', backref=db.backref('purchases', lazy=True))
    supplier = db.relationship('Supplier', backref=db.backref('supplied_books', lazy=True))
    employee = db.relationship('Employee', backref=db.backref('sales', lazy=True))