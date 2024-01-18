
from flask import Blueprint, request, jsonify, abort
from models.supplier import db, Supplier

supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    supplier_list = [{'id': sup.id, 'name': sup.name, 'contact_info': sup.contact_info} for sup in suppliers]
    return jsonify({'suppliers': supplier_list})

@supplier_bp.route('/', methods=['POST'])
def create_supplier():
    data = request.get_json()
    new_supplier = Supplier(**data)

    try:
        db.session.add(new_supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier created successfully', 'supplier_id': new_supplier.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier_data = {'id': supplier.id, 'name': supplier.name, 'contact_info': supplier.contact_info}
    return jsonify({'supplier': supplier_data})

@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = request.get_json()

    try:
        for key, value in data.items():
            setattr(supplier, key, value)

        db.session.commit()
        return jsonify({'message': 'Supplier updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)

    try:
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
