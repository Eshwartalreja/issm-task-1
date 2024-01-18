# routes/customer_routes.py
from flask import Blueprint, request, jsonify, abort
from models.customer import db, Customer

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(**data)

    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    customer_list = [{'id': customer.id, 'name': customer.name, 'contact_details': customer.contact_details} for customer in customers]
    return jsonify({'customers': customer_list})

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        abort(404, description=f'customer {customer_id} not found')
    return jsonify({'id': customer.id, 'name': customer.name, 'contact_details': customer.contact_details})

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        abort(404, description=f'customer {customer_id} not found')
    
    data = request.get_json()

    try:
        for key, value in data.items():
            setattr(customer, key, value)

        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>/purchases', methods=['GET'])
def get_customer_purchases(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_books = customer.purchases
    purchase_list = [{'book_id': book.id, 'title': book.title, 'author': book.author, 'isbn': book.isbn, 'price': book.price, 'quantity': book.quantity} for book in customer_books]
    return jsonify({'customer_purchases': purchase_list})