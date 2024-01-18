
from flask import Blueprint, request, jsonify, abort
from models.employee import db, Employee

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_list = [{'id': emp.id, 'name': emp.name, 'contact_details': emp.contact_details, 'role': emp.role} for emp in employees]
    return jsonify({'employees': employee_list})

@employee_bp.route('/', methods=['POST'])
def create_employee():
    data = request.get_json()
    new_employee = Employee(**data)

    try:
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({'message': 'Employee created successfully', 'employee_id': new_employee.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@employee_bp.route('/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee_data = {'id': employee.id, 'name': employee.name, 'contact_details': employee.contact_details, 'role': employee.role}
    return jsonify({'employee': employee_data})

@employee_bp.route('/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()

    try:
        for key, value in data.items():
            setattr(employee, key, value)

        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employee_bp.route('/<int:employee_id>/total_books_sold', methods=['GET'])
def get_total_books_sold(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    employee_books = employee.sales
    total_books_sold = sum(book.quantity for book in employee_books)
    return jsonify({'total_books_sold': total_books_sold})