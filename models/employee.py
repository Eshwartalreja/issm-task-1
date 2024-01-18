from utils.db_utils import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_details = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), nullable=False)