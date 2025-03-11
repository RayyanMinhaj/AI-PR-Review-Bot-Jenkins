from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from io import BytesIO
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps
import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Security Configuration
app.config['SECRET_KEY'] = secrets.token_hex(24)
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Define the UserGroup model
class UserGroup(db.Model):
    __tablename__ = 'user_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserGroup {self.name}>'

class GroupOperatorSettings(db.Model):
    __tablename__ = 'group_operator_settings'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('user_groups.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    system_access = db.Column(Boolean, default=False)
    management_access = db.Column(Boolean, default=False)
    data_access = db.Column(Boolean, default=False)
    information_service = db.Column(Boolean, default=False)
    client = db.Column(Boolean, default=False)
    contract_voucher_only = db.Column(Boolean, default=False)
    view_contract = db.Column(Boolean, default=False)
    view_client = db.Column(Boolean, default=False)
    view_supplier = db.Column(Boolean, default=False)
    parameter = db.Column(Boolean, default=False)
    exchange_rate_currency = db.Column(Boolean, default=False)
    archive_access = db.Column(Boolean, default=False)
    archive_right = db.Column(Boolean, default=False)
    backup = db.Column(Boolean, default=False)
    export_quot_tour = db.Column(Boolean, default=False)
    import_quot_tour = db.Column(Boolean, default=False)
    modify_quot_site = db.Column(Boolean, default=False)
    modify_tour_site = db.Column(Boolean, default=False)
    export_data = db.Column(Boolean, default=False)
    import_data = db.Column(Boolean, default=False)
    import_location = db.Column(Boolean, default=False)
    ambo_travcom_sage_export = db.Column(Boolean, default=False)
    resrequest_parameter = db.Column(Boolean, default=False)
    operation_access = db.Column(Boolean, default=False)
    accounts_access = db.Column(Boolean, default=False)
    print_documents_access = db.Column(Boolean, default=False)
    note_access = db.Column(Boolean, default=False)
    invoice_warning_access = db.Column(Boolean, default=False)
    authors_access = db.Column(Boolean, default=False)
    quotation = db.Column(Boolean, default=False)
    quotation_owner = db.Column(Boolean, default=False)
    view_tour = db.Column(Boolean, default=False)
    manual_cost = db.Column(Boolean, default=False)
    change_use_sale_price_to_use_nett_cost = db.Column(Boolean, default=False)
    resrequest = db.Column(Boolean, default=False)
    account = db.Column(Boolean, default=False)
    voucher_cost = db.Column(Boolean, default=False)
    payment = db.Column(Boolean, default=False)
    cheque_no = db.Column(Boolean, default=False)
    park_payment = db.Column(Boolean, default=False)
    financial_analysis = db.Column(Boolean, default=False)
    unlock_payment = db.Column(Boolean, default=False)
    modify_cost_of_voucher = db.Column(Boolean, default=False)
    delete_payment = db.Column(Boolean, default=False)
    invoice_tour = db.Column(Boolean, default=False)
    invoice_list = db.Column(Boolean, default=False)
    invoice_statement = db.Column(Boolean, default=False)
    invoice_title = db.Column(Boolean, default=False)
    invoice_code_item_sage = db.Column(Boolean, default=False)
    invoice_validate = db.Column(Boolean, default=False)
    invoice_unlock = db.Column(Boolean, default=False)
    invoice_proforma_only = db.Column(Boolean, default=False)
    receipt = db.Column(Boolean, default=False)
    receipt_validate = db.Column(Boolean, default=False)
    link_invoice_to_receipt = db.Column(Boolean, default=False)
    receipt_unlock = db.Column(Boolean, default=False)
    print_invoice_windows = db.Column(Boolean, default=False)
    percentage_on_invoice_items = db.Column(Boolean, default=False)
    change_tax_rule_to_use = db.Column(Boolean, default=False)
    # Print Document Settings
    presentation_annotation = db.Column(Boolean, default=False)
    presentation_duplicate = db.Column(Boolean, default=False)
    presentation_email = db.Column(Boolean, default=False)
    presentation_email_pdf = db.Column(Boolean, default=False)
    presentation_excel = db.Column(Boolean, default=False)
    presentation_html = db.Column(Boolean, default=False)
    presentation_pdf = db.Column(Boolean, default=False)
    presentation_printer = db.Column(Boolean, default=False)
    presentation_word = db.Column(Boolean, default=False)
    presentation_xml = db.Column(Boolean, default=False)

    invoice_annotation = db.Column(Boolean, default=False)
    invoice_duplicate = db.Column(Boolean, default=False)
    invoice_email = db.Column(Boolean, default=False)
    invoice_email_pdf = db.Column(Boolean, default=False)
    invoice_excel = db.Column(Boolean, default=False)
    invoice_html = db.Column(Boolean, default=False)
    invoice_pdf = db.Column(Boolean, default=False)
    invoice_printer = db.Column(Boolean, default=False)
    invoice_word = db.Column(Boolean, default=False)
    invoice_xml = db.Column(Boolean, default=False)

    voucher_annotation = db.Column(Boolean, default=False)
    voucher_duplicate = db.Column(Boolean, default=False)
    voucher_email = db.Column(Boolean, default=False)
    voucher_email_pdf = db.Column(Boolean, default=False)
    voucher_excel = db.Column(Boolean, default=False)
    voucher_html = db.Column(Boolean, default=False)
    voucher_pdf = db.Column(Boolean, default=False)
    voucher_printer = db.Column(Boolean, default=False)
    voucher_word = db.Column(Boolean, default=False)
    voucher_xml = db.Column(Boolean, default=False)

    other_annotation = db.Column(Boolean, default=False)
    other_duplicate = db.Column(Boolean, default=False)
    other_email = db.Column(Boolean, default=False)
    other_email_pdf = db.Column(Boolean, default=False)
    other_excel = db.Column(Boolean, default=False)
    other_html = db.Column(Boolean, default=False)
    other_pdf = db.Column(Boolean, default=False)
    other_printer = db.Column(Boolean, default=False)
    other_word = db.Column(Boolean, default=False)
    other_xml = db.Column(Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    group = relationship('UserGroup', backref=db.backref('settings', uselist=False))

class GroupOperatorNote(db.Model):
    __tablename__ = 'group_operator_notes'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('user_groups.id'), nullable=False)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    group = relationship('UserGroup', backref=db.backref('note', uselist=False))

class InvoiceWarningSettings(db.Model):
    __tablename__ = 'invoice_warning_settings'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('user_groups.id'), nullable=False)
    invoice_warning = db.Column(Boolean, default=False)
    include_proforma = db.Column(Boolean, default=False)
    include_credit_note = db.Column(Boolean, default=False)
    include_invoices_of_all_operators = db.Column(Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    number_of_days = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    group = relationship('UserGroup', backref=db.backref('invoice_warning', uselist=False))

class AuthorDetails(db.Model):
    __tablename__ = 'author_details'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('user_groups.id'), nullable=False)
    created_by = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)
    revised_by = db.Column(db.String(80), nullable=True)
    revised_on = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    group = relationship('UserGroup', backref=db.backref('author_details', uselist=False))

    def __repr__(self):
        return f'<AuthorDetails {self.group_id}>'

# Create database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Function to handle errors
def handle_error(message, code):
    return jsonify({'message': message}), code

# Function to validate input data
def validate_input(data, required_fields):
    for field in required_fields:
        if field not in data or not data[field]:
            return f'{field} is required', 400
    return None, None

# Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        user = User.query.filter_by(username='admin').first()
        if not user or token != user.password_hash:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function

# Admin check decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        user = User.query.filter_by(username='admin').first()
        if not user or token != user.password_hash or not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403

        return f(*args, **kwargs)
    return decorated_function

# User Registration (Admin only)
@app.route('/api/register', methods=['POST'])
@admin_required
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    error_message, error_code = validate_input(data, ['username', 'password'])
    if error_message:
        return handle_error(error_message, error_code)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return handle_error('Username already exists', 400)

    try:
        new_user = User(username=username, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    error_message, error_code = validate_input(data, ['username', 'password'])
    if error_message:
        return handle_error(error_message, error_code)

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return handle_error('Invalid username or password', 401)

    return jsonify({'token': user.password_hash, 'is_admin': user.is_admin}), 200

# API Endpoints

# Endpoint to create a new group
@app.route('/api/groups', methods=['POST'])
@token_required
@admin_required
def create_group():
    data = request.get_json()
    name = data.get('name')

    error_message, error_code = validate_input(data, ['name'])
    if error_message:
        return handle_error(error_message, error_code)

    existing_group = UserGroup.query.filter_by(name=name).first()
    if existing_group:
        return handle_error('Group name already exists', 400)

    try:
        new_group = UserGroup(name=name)
        db.session.add(new_group)
        db.session.commit()
        return jsonify({'id': new_group.id, 'name': new_group.name}), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to browse existing groups
@app.route('/api/groups', methods=['GET'])
@token_required
def browse_groups():
    try:
        groups = UserGroup.query.all()
        return jsonify([{'id': group.id, 'name': group.name} for group in groups])
    except Exception as e:
        return handle_error(str(e), 500)

# Endpoint to get a specific group by ID
@app.route('/api/groups/<int:group_id>', methods=['GET'])
@token_required
def get_group(group_id):
    try:
        group = UserGroup.query.get_or_404(group_id)
        return jsonify({'id': group.id, 'name': group.name})
    except Exception as e:
        return handle_error(str(e), 404)

# Endpoint to update an existing group
@app.route('/api/groups/<int:group_id>', methods=['PUT'])
@token_required
@admin_required
def update_group(group_id):
    group = UserGroup.query.get_or_404(group_id)
    data = request.get_json()
    name = data.get('name')

    error_message, error_code = validate_input(data, ['name'])
    if error_message:
        return handle_error(error_message, error_code)

    existing_group = UserGroup.query.filter_by(name=name).first()
    if existing_group and existing_group.id != group_id:
        return handle_error('Group name already exists', 400)

    try:
        group.name = name
        group.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'id': group.id, 'name': group.name})
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to delete a group
@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_group(group_id):
    group = UserGroup.query.get_or_404(group_id)
    try:
        db.session.delete(group)
        db.session.commit()
        return jsonify({'message': 'Group deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to print list of groups
@app.route('/api/groups/print', methods=['GET'])
@token_required
def print_groups():
    try:
        groups = UserGroup.query.all()
        group_list = "\n".join([f"ID: {group.id}, Name: {group.name}" for group in groups])
        output = BytesIO()
        output.write(group_list.encode('utf-8'))
        output.seek(0)
        return send_file(output, mimetype='text/plain', as_attachment=True, download_name='groups.txt')
    except Exception as e:
        return handle_error(str(e), 500)

# Endpoint to update group operator settings
@app.route('/api/groups/<int:group_id>/settings', methods=['PUT'])
@token_required
@admin_required
def update_group_settings(group_id):
    group = UserGroup.query.get_or_404(group_id)
    data = request.get_json()

    try:
        settings = GroupOperatorSettings.query.filter_by(group_id=group_id).first()
        if not settings:
            settings = GroupOperatorSettings(group_id=group_id, name=group.name)
            db.session.add(settings)

        settings.name = data.get('name', settings.name)
        settings.system_access = data.get('system_access', settings.system_access)
        settings.management_access = data.get('management_access', settings.management_access)
        settings.data_access = data.get('data_access', settings.data_access)
        settings.information_service = data.get('information_service', settings.information_service)
        settings.client = data.get('client', settings.client)
        settings.contract_voucher_only = data.get('contract_voucher_only', settings.contract_voucher_only)
        settings.view_contract = data.get('view_contract', settings.view_contract)
        settings.view_client = data.get('view_client', settings.view_client)
        settings.view_supplier = data.get('view_supplier', settings.view_supplier)
        settings.parameter = data.get('parameter', settings.parameter)
        settings.exchange_rate_currency = data.get('exchange_rate_currency', settings.exchange_rate_currency)
        settings.archive_access = data.get('archive_access', settings.archive_access)
        settings.archive_right = data.get('archive_right', settings.archive_right)
        settings.backup = data.get('backup', settings.backup)
        settings.export_quot_tour = data.get('export_quot_tour', settings.export_quot_tour)
        settings.import_quot_tour = data.get('import_quot_tour', settings.import_quot_tour)
        settings.modify_quot_site = data.get('modify_quot_site', settings.modify_quot_site)
        settings.modify_tour_site = data.get('modify_tour_site', settings.modify_tour_site)
        settings.export_data = data.get('export_data', settings.export_data)
        settings.import_data = data.get('import_data', settings.import_data)
        settings.import_location = data.get('import_location', settings.import_location)
        settings.ambo_travcom_sage_export = data.get('ambo_travcom_sage_export', settings.ambo_travcom_sage_export)
        settings.resrequest_parameter = data.get('resrequest_parameter', settings.resrequest_parameter)
        settings.operation_access = data.get('operation_access', settings.operation_access)
        settings.accounts_access = data.get('accounts_access', settings.accounts_access)
        settings.print_documents_access = data.get('print_documents_access', settings.print_documents_access)
        settings.note_access = data.get('note_access', settings.note_access)
        settings.invoice_warning_access = data.get('invoice_warning_access', settings.invoice_warning_access)
        settings.authors_access = data.get('authors_access', settings.authors_access)
        settings.quotation = data.get('quotation', settings.quotation)
        settings.quotation_owner = data.get('quotation_owner', settings.quotation_owner)
        settings.view_tour = data.get('view_tour', settings.view_tour)
        settings.manual_cost = data.get('manual_cost', settings.manual_cost)
        settings.change_use_sale_price_to_use_nett_cost = data.get('change_use_sale_price_to_use_nett_cost', settings.change_use_sale_price_to_use_nett_cost)
        settings.resrequest = data.get('resrequest', settings.resrequest)
        settings.account = data.get('account', settings.account)
        settings.voucher_cost = data.get('voucher_cost', settings.voucher_cost)
        settings.payment = data.get('payment', settings.payment)
        settings.cheque_no = data.get('cheque_no', settings.cheque_no)
        settings.park_payment = data.get('park_payment', settings.park_payment)
        settings.financial_analysis = data.get('financial_analysis', settings.financial_analysis)
        settings.unlock_payment = data.get('unlock_payment', settings.unlock_payment)
        settings.modify_cost_of_voucher = data.get('modify_cost_of_voucher', settings.modify_cost_of_voucher)
        settings.delete_payment = data.get('delete_payment', settings.delete_payment)
        settings.invoice_tour = data.get('invoice_tour', settings.invoice_tour)
        settings.invoice_list = data.get('invoice_list', settings.invoice_list)
        settings.invoice_statement = data.get('invoice_statement', settings.invoice_statement)
        settings.invoice_title = data.get('invoice_title', settings.invoice_title)
        settings.invoice_code_item_sage = data.get('invoice_code_item_sage', settings.invoice_code_item_sage)
        settings.invoice_validate = data.get('invoice_validate', settings.invoice_validate)
        settings.invoice_unlock = data.get('invoice_unlock', settings.invoice_unlock)
        settings.invoice_proforma_only = data.get('invoice_proforma_only', settings.invoice_proforma_only)
        settings.receipt = data.get('receipt', settings.receipt)
        settings.receipt_validate = data.get('receipt_validate', settings.receipt_validate)
        settings.link_invoice_to_receipt = data.get('link_invoice_to_receipt', settings.link_invoice_to_receipt)
        settings.receipt_unlock = data.get('receipt_unlock', settings.receipt_unlock)
        settings.print_invoice_windows = data.get('print_invoice_windows', settings.print_invoice_windows)
        settings.percentage_on_invoice_items = data.get('percentage_on_invoice_items', settings.percentage_on_invoice_items)
        settings.change_tax_rule_to_use = data.get('change_tax_rule_to_use', settings.change_tax_rule_to_use)

        # Print Document Settings
        settings.presentation_annotation = data.get('presentation_annotation', settings.presentation_annotation)
        settings.presentation_duplicate = data.get('presentation_duplicate', settings.presentation_duplicate)
        settings.presentation_email = data.get('presentation_email', settings.presentation_email)
        settings.presentation_email_pdf = data.get('presentation_email_pdf', settings.presentation_email_pdf)
        settings.presentation_excel = data.get('presentation_excel', settings.presentation_excel)
        settings.presentation_html = data.get('presentation_html', settings.presentation_html)
        settings.presentation_pdf = data.get('presentation_pdf', settings.presentation_pdf)
        settings.presentation_printer = data.get('presentation_printer', settings.presentation_printer)
        settings.presentation_word = data.get('presentation_word', settings.presentation_word)
        settings.presentation_xml = data.get('presentation_xml', settings.presentation_xml)

        settings.invoice_annotation = data.get('invoice_annotation', settings.invoice_annotation)
        settings.invoice_duplicate = data.get('invoice_duplicate', settings.invoice_duplicate)
        settings.invoice_email = data.get('invoice_email', settings.invoice_email)
        settings.invoice_email_pdf = data.get('invoice_email_pdf', settings.invoice_email_pdf)
        settings.invoice_excel = data.get('invoice_excel', settings.invoice_excel)
        settings.invoice_html = data.get('invoice_html', settings.invoice_html)
        settings.invoice_pdf = data.get('invoice_pdf', settings.invoice_pdf)
        settings.invoice_printer = data.get('invoice_printer', settings.invoice_printer)
        settings.invoice_word = data.get('invoice_word', settings.invoice_word)
        settings.invoice_xml = data.get('invoice_xml', settings.invoice_xml)

        settings.voucher_annotation = data.get('voucher_annotation', settings.voucher_annotation)
        settings.voucher_duplicate = data.get('voucher_duplicate', settings.voucher_duplicate)
        settings.voucher_email = data.get('voucher_email', settings.voucher_email)
        settings.voucher_email_pdf = data.get('voucher_email_pdf', settings.voucher_email_pdf)
        settings.voucher_excel = data.get('voucher_excel', settings.voucher_excel)
        settings.voucher_html = data.get('voucher_html', settings.voucher_html)
        settings.voucher_pdf = data.get('voucher_pdf', settings.voucher_pdf)
        settings.voucher_printer = data.get('voucher_printer', settings.voucher_printer)
        settings.voucher_word = data.get('voucher_word', settings.voucher_word)
        settings.voucher_xml = data.get('voucher_xml', settings.voucher_xml)

        settings.other_annotation = data.get('other_annotation', settings.other_annotation)
        settings.other_duplicate = data.get('other_duplicate', settings.other_duplicate)
        settings.other_email = data.get('other_email', settings.other_email)
        settings.other_email_pdf = data.get('other_email_pdf', settings.other_email_pdf)
        settings.other_excel = data.get('other_excel', settings.other_excel)
        settings.other_html = data.get('other_html', settings.other_html)
        settings.other_pdf = data.get('other_pdf', settings.other_pdf)
        settings.other_printer = data.get('other_printer', settings.other_printer)
        settings.other_word = data.get('other_word', settings.other_word)
        settings.other_xml = data.get('other_xml', settings.other_xml)

        settings.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Group settings updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to get group operator settings
@app.route('/api/groups/<int:group_id>/settings', methods=['GET'])
@token_required
def get_group_settings(group_id):
    group = UserGroup.query.get_or_404(group_id)
    try:
        settings = GroupOperatorSettings.query.filter_by(group_id=group_id).first()
        if not settings:
            return jsonify({'message': 'No settings found for this group'}), 404

        return jsonify({
            'id': settings.id,
            'group_id': settings.group_id,
            'name': settings.name,
            'system_access': settings.system_access,
            'management_access': settings.management_access,
            'data_access': settings.data_access,
            'information_service': settings.information_service,
            'client': settings.client,
            'contract_voucher_only': settings.contract_voucher_only,
            'view_contract': settings.view_contract,
            'view_client': settings.view_client,
            'view_supplier': settings.view_supplier,
            'parameter': settings.parameter,
            'exchange_rate_currency': settings.exchange_rate_currency,
            'archive_access': settings.archive_access,
            'archive_right': settings.archive_right,
            'backup': settings.backup,
            'export_quot_tour': settings.export_quot_tour,
            'import_quot_tour': settings.import_quot_tour,
            'modify_quot_site': settings.modify_quot_site,
            'modify_tour_site': settings.modify_tour_site,
            'export_data': settings.export_data,
            'import_data': settings.import_data,
            'import_location': settings.import_location,
            'ambo_travcom_sage_export': settings.ambo_travcom_sage_export,
            'resrequest_parameter': settings.resrequest_parameter,
            'operation_access': settings.operation_access,
            'accounts_access': settings.accounts_access,
            'print_documents_access': settings.print_documents_access,
            'note_access': settings.note_access,
            'invoice_warning_access': settings.invoice_warning_access,
            'authors_access': settings.authors_access,
            'quotation': settings.quotation,
            'quotation_owner': settings.quotation_owner,
            'view_tour': settings.view_tour,
            'manual_cost': settings.manual_cost,
            'change_use_sale_price_to_use_nett_cost': settings.change_use_sale_price_to_use_nett_cost,
            'resrequest': settings.resrequest,
            'account': settings.account,
            'voucher_cost': settings.voucher_cost,
            'payment': settings.payment,
            'cheque_no': settings.cheque_no,
            'park_payment': settings.park_payment,
            'financial_analysis': settings.financial_analysis,
            'unlock_payment': settings.unlock_payment,
            'modify_cost_of_voucher': settings.modify_cost_of_voucher        'delete_payment': settings.delete_payment,
            'invoice_tour': settings.invoice_tour,
            'invoice_list': settings.invoice_list,
            'invoice_statement': settings.invoice_statement,
            'invoice_title': settings.invoice_title,
            'invoice_code_item_sage': settings.invoice_code_item_sage,
            'invoice_validate': settings.invoice_validate,
            'invoice_unlock': settings.invoice_unlock,
            'invoice_proforma_only': settings.invoice_proforma_only,
            'receipt': settings.receipt,
            'receipt_validate': settings.receipt_validate,
            'link_invoice_to_receipt': settings.link_invoice_to_receipt,
            'receipt_unlock': settings.receipt_unlock,
            'print_invoice_windows': settings.print_invoice_windows,
            'percentage_on_invoice_items': settings.percentage_on_invoice_items,
        'change_tax_rule_to_use': settings.change_tax_rule_to_use,
            # Print Document Settings
            'presentation_annotation': settings.presentation_annotation,
            'presentation_duplicate': settings.presentation_duplicate,
            'presentation_email': settings.presentation_email,
            'presentation_email_pdf': settings.presentation_email_pdf,
            'presentation_excel': settings.presentation_excel,
            'presentation_html': settings.presentation_html,
            'presentation_pdf': settings.presentation_pdf,
            'presentation_printer': settings.presentation_printer,
            'presentation_word': settings.presentation_word,
            'presentation_xml': settings.presentation_xml,

            'invoice_annotation': settings.invoice_annotation,
            'invoice_duplicate': settings.invoice_duplicate,
            'invoice_email': settings.invoice_email,
            'invoice_email_pdf': settings.invoice_email_pdf,
            'invoice_excel': settings.invoice_excel,
            'invoice_html': settings.invoice_html,
            'invoice_pdf': settings.invoice_pdf,
            'invoice_printer': settings.invoice_printer,
            'invoice_word': settings.invoice_word,
            'invoice_xml': settings.invoice_xml,

            'voucher_annotation': settings.voucher_annotation,
            'voucher_duplicate': settings.voucher_duplicate,
            'voucher_email': settings.voucher_email,
            'voucher_email_pdf': settings.voucher_email_pdf,
            'voucher_excel': settings.voucher_excel,
            'voucher_html': settings.voucher_html,
            'voucher_pdf': settings.voucher_pdf,
            'voucher_printer': settings.voucher_printer,
            'voucher_word': settings.voucher_word,
            'voucher_xml': settings.voucher_xml,

            'other_annotation': settings.other_annotation,
            'other_duplicate': settings.other_duplicate,
            'other_email': settings.other_email,
            'other_email_pdf': settings.other_email_pdf,
            'other_excel': settings.other_excel,
            'other_html': settings.other_html,
            'other_pdf': settings.other_pdf,
            'other_printer': settings.other_printer,
            'other_word': settings.other_word,
            'other_xml': settings.other_xml,
    'invoice_warning': invoice_warning_settings.invoice_warning,
            'include_proforma': invoice_warning_settings.include_proforma,
            'include_credit_note': invoice_warning_settings.include_credit_note,
            'include_invoices_of_all_operators': invoice_warning_settings.include_invoices_of_all_operators,
            'due_date': invoice_warning_settings.due_date,
            'number_of_days': invoice_warning_settings.number_of_days

        }), 200
    except Exception as e:
        return handle_error(str(e), 500)

# Endpoint to reset group operator settings to default
@app.route('/api/groups/<int:group_id>/settings/default', methods=['PUT'])
@token_required
@admin_required
def reset_group_settings(group_id):
    group = UserGroup.query.get_or_404(group_id)
    try:
        settings = GroupOperatorSettings.query.filter_by(group_id=group_id).first()
        if not settings:
            settings = GroupOperatorSettings(group_id=group_id, name=group.name)
            db.session.add(settings)

        # Reset settings to default values
        settings.name = group.name
        settings.system_access = False
        settings.management_access = False
        settings.data_access = False
        settings.information_service = False
        settings.client = False
        settings.contract_voucher_only = False
        settings.view_contract = False
        settings.view_client = False
        settings.view_supplier = False
        settings.parameter = False
        settings.exchange_rate_currency = False
        settings.archive_access = False
        settings.archive_right = False
        settings.backup = False
        settings.export_quot_tour = False
        settings.import_quot_tour = False
        settings.modify_quot_site = False
        settings.modify_tour_site = False
        settings.export_data = False
        settings.import_data = False
        settings.import_location = False
        settings.ambo_travcom_sage_export = False
        settings.resrequest_parameter = False
        settings.operation_access = False
        settings.accounts_access = False
        settings.print_documents_access = False
        settings.note_access = False
        settings.invoice_warning_access = False
        settings.authors_access = False
        settings.quotation = False
        settings.quotation_owner = False
        settings.view_tour = False
        settings.manual_cost = False
        settings.change_use_sale_price_to_use_nett_cost = False
        settings.resrequest = False
        settings.account = False
        settings.voucher_cost = False
        settings.payment = False
        settings.cheque_no = False
        settings.park_payment = False
        settings.financial_analysis = False
        settings.unlock_payment = False
        settings.modify_cost_of_voucher = False
        settings.delete_payment = False
        settings.invoice_tour = False
        settings.invoice_list = False
        settings.invoice_statement = False
        settings.invoice_title = False
        settings.invoice_code_item_sage = False
        settings.invoice_validate = False
        settings.invoice_unlock = False
        settings.invoice_proforma_only = False
        settings.receipt = False
        settings.receipt_validate = False
        settings.link_invoice_to_receipt = False
        settings.receipt_unlock = False
        settings.print_invoice_windows = False
        settings.percentage_on_invoice_items = False
        settings.change_tax_rule_to_use = False

        # Reset Print Document Settings
        settings.presentation_annotation = False
        settings.presentation_duplicate = False
        settings.presentation_email = False
        settings.presentation_email_pdf = False
        settings.presentation_excel = False
        settings.presentation_html = False
        settings.presentation_pdf = False
        settings.presentation_printer = False
        settings.presentation_word = False
        settings.presentation_xml = False

        settings.invoice_annotation = False
        settings.invoice_duplicate = False
        settings.invoice_email = False
        settings.invoice_email_pdf = False
        settings.invoice_excel = False
        settings.invoice_html = False
        settings.invoice_pdf = False
        settings.invoice_printer = False
        settings.invoice_word = False
        settings.invoice_xml = False

        settings.voucher_annotation = False
        settings.voucher_duplicate = False
        settings.voucher_email = False
        settings.voucher_email_pdf = False
        settings.voucher_excel = False
        settings.voucher_html = False
        settings.voucher_pdf = False
        settings.voucher_printer = False
        settings.voucher_word = False
        settings.voucher_xml = False

        settings.other_annotation = False
        settings.other_duplicate = False
        settings.other_email = False
        settings.other_email_pdf = False
        settings.other_excel = False
        settings.other_html = False
        settings.other_pdf = False
        settings.other_printer = False
        settings.other_word = False
        settings.other_xml = False

        settings.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Group settings reset to default successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to update group operator note
@app.route('/api/groups/<int:group_id>/note', methods=['PUT'])
@token_required
@admin_required
def update_group_note(group_id):
    group = UserGroup.query.get_or_404(group_id)
    data = request.get_json()
    note = data.get('note')

    try:
        group_note = GroupOperatorNote.query.filter_by(group_id=group_id).first()
        if not group_note:
            group_note = GroupOperatorNote(group_id=group_id)
            db.session.add(group_note)

        group_note.note = note
        group_note.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Group note updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to get group operator note
@app.route('/api/groups/<int:group_id>/note', methods=['GET'])
@token_required
def get_group_note(group_id):
    group = UserGroup.query.get_or_404(group_id)
    try:
        group_note = GroupOperatorNote.query.filter_by(group_id=group_id).first()
        if not group_note:
            return jsonify({'note': None}), 200  # Return None if no note exists

        return jsonify({'note': group_note.note}), 200
    except Exception as e:
        return handle_error(str(e), 500)

# Endpoint to update invoice warning settings
@app.route('/api/groups/<int:group_id>/invoice_warning', methods=['PUT'])
@token_required
@admin_required
def update_invoice_warning_settings(group_id):
    group = UserGroup.query.get_or_404(group_id)
    data = request.get_json()

    try:
        invoice_warning_settings = InvoiceWarningSettings.query.filter_by(group_id=group_id).first()
        if not invoice_warning_settings:
            invoice_warning_settings = InvoiceWarningSettings(group_id=group_id)
            db.session.add(invoice_warning_settings)

        invoice_warning_settings.invoice_warning = data.get('invoice_warning', invoice_warning_settings.invoice_warning)
        invoice_warning_settings.include_proforma = data.get('include_proforma', invoice_warning_settings.include_proforma)
        invoice_warning_settings.include_credit_note = data.get('include_credit_note', invoice_warning_settings.include_credit_note)
        invoice_warning_settings.include_invoices_of_all_operators = data.get('include_invoices_of_all_operators', invoice_warning_settings.include_invoices_of_all_operators)

        due_date_str = data.get('due_date')
        invoice_warning_settings.due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M:%S') if due_date_str else None

        invoice_warning_settings.number_of_days = data.get('number_of_days', invoice_warning_settings.number_of_days)
        invoice_warning_settings.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Invoice warning settings updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to get invoice warning settings
@app.route('/api/groups/<int:group_id>/invoice_warning', methods=['GET'])
@token_required
def get_invoice_warning_settings(group_id):
    group = UserGroup.query.get_or_404(group_id)
    try:
        invoice_warning_settings = InvoiceWarningSettings.query.filter_by(group_id=group_id).first()
        if not invoice_warning_settings:
            return jsonify({
'invoice_warning': None,
'include_proforma': None,
'include_credit_note': None,
'include_invoices_of_all_operators': None,
'due_date': None,
'number_of_days': None
            }), 200

        return jsonify({
            'invoice_warning': invoice_warning_settings.invoice_warning,
            'include_proforma': invoice_warning_settings.include_proforma,
            'include_credit_note': invoice_warning_settings.include_credit_note,
            'include_invoices_of_all_operators': invoice_warning_settings.include_invoices_of_all_operators,
            'due_date': invoice_warning_settings.due_date,
            'number_of_days': invoice_warning_settings.number_of_days
        }), 200
    except Exception as e:
        return handle_error(str(e), 500)

# Endpoint to update author details
@app.route('/api/groups/<int:group_id>/author_details', methods=['PUT'])
@token_required
@admin_required
def update_author_details(group_id):
    group = UserGroup.query.get_or_404(group_id)
    data = request.get_json()

    try:
        author_details = AuthorDetails.query.filter_by(group_id=group_id).first()
        if not author_details:
            author_details = AuthorDetails(group_id=group_id)
            db.session.add(author_details)

        author_details.created_by = data.get('created_by', author_details.created_by)

        created_on_str = data.get('created_on')
        author_details.created_on = datetime.strptime(created_on_str, '%Y-%m-%dT%H:%M:%S') if created_on_str else None

        author_details.revised_by = data.get('revised_by', author_details.revised_by)

        revised_on_str = data.get('revised_on')
        author_details.revised_on = datetime.strptime(revised_on_str, '%Y-%m-%dT%H:%M:%S') if revised_on_str else None

        author_details.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({'message': 'Author details updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(str(e), 500)

# Endpoint to get author details
@app.route('/api/groups/<int:group_id>/author_details', methods=['GET'])
@token_required
def get_author_details(group_id):
    group = UserGroup.query.get_or_404(group_id)
    try:
        author_details = AuthorDetails.query.filter_by(group_id=group_id).first()
        if not author_details:
            return jsonify({
'created_by': None,
'created_on': None,
'revised_by': None,
'revised_on': None
            }), 200

        return jsonify({
            'created_by': author_details.created_by,
            'created_on': author_details.created_on.isoformat() if author_details.created_on else None,
            'revised_by': author_details.revised_by,
            'revised_on': author_details.revised_on.isoformat() if author_details.revised_on else None
        }), 200
    except Exception as e:
        return handle_error(str(e), 500)

# Navigation Endpoints
@app.route('/api/menu/data', methods=['GET'])
@token_required
def navigate_data():
    return jsonify({'message': 'Navigated to Data module'})

@app.route('/api/menu/quotation', methods=['GET'])
@token_required
def navigate_quotation():
    return jsonify({'message': 'Navigated to Quotation module'})

@app.route('/api/menu/tour', methods=['GET'])
@token_required
def navigate_tour():
    return jsonify({'message': 'Navigated to Tour module'})

@app.route('/api/menu/payment', methods=['GET'])
@token_required
def navigate_payment():
    return jsonify({'message': 'Navigated to Payment module'})

@app.route('/api/menu/invoice', methods=['GET'])
@token_required
def navigate_invoice():
    return jsonify({'message': 'Navigated to Invoice module'})

if __name__ == '__main__':
    app.run(debug=True)
