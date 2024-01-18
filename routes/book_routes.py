
from flask import Blueprint, request, jsonify,abort
from models.book import db,Book
from models.customer import Customer
from models.employee import Employee

book_bp = Blueprint('book', __name__)


@book_bp.route('/', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(**data)

    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@book_bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{'title': book.title, 'author': book.author, 'isbn': book.isbn, 'price': book.price, 'quantity': book.quantity, "Book Id": book.id,"Supplier Id":book.supplier_id,"Employee Id":book.employee_id,"customer Id":book.customer_id} for book in books]
    return jsonify({'books': book_list})

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)

    if book is None:
        abort(404, description=f'Book with ID {book_id} not found')
    
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'isbn': book.isbn, 'price': book.price, 'quantity': book.quantity})


@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)

    data = request.get_json()

    if book is None:
        abort(404, description=f'Book with ID {book_id} not found')

    try:
        for key, value in data.items():
            setattr(book, key, value)

        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    


@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    


@book_bp.route('/sell/<int:book_id>', methods=['POST'])
def sell_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    try:
        if book.quantity < data['quantity']:
            return jsonify({'error': 'Not enough stock available'}), 400

        
        book.quantity -= data['quantity']

        
        customer_id = data.get('customer_id')
        if customer_id:
            customer = Customer.query.get_or_404(customer_id)
            customer.name = data.get('customer_name', customer.name)
            customer.contact_details = data.get('customer_contact_details', customer.contact_details)
        else:
            customer = Customer(name=data['customer_name'], contact_details=data['customer_contact_details'])
            db.session.add(customer)

        
        employee_id = data.get('employee_id')
        if employee_id:
            employee = Employee.query.get_or_404(employee_id)
            book.employee = employee

        
        book.customer = customer
        db.session.commit()

        return jsonify({'message': 'Sale processed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
