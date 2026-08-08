from flask import Blueprint, render_template, request, redirect, url_for,flash
from sqlalchemy import all_
from app.services.student_import_service import mark_payment
from app.utils.validators import is_allowed_excel_file
from app.services.student_import_service import parse_excel, save_students, ExcelParseError
from app.models.model import Student,Payment
from app.services.ai_reminder_service import generate_reminder_message
students_bp = Blueprint('students', __name__, url_prefix='/students')
app_bp = Blueprint('app', __name__, url_prefix='')
@app_bp.route('/')
@students_bp.route('/upload', methods=['GET'])
def upload_page():
    return render_template('students/upload.html')

@students_bp.route('/upload', methods=['POST'])
def handle_upload():
    uploaded_file = request.files.get('file')
    if uploaded_file is None or uploaded_file.filename == '':
        flash('No file selected for uploading', 'error')
        return redirect(url_for('students.upload_page'))

    if not is_allowed_excel_file(uploaded_file.filename):
        flash('Invalid file type. Please upload an Excel file.', 'error')
        return redirect(url_for('students.upload_page'))

    try:
        df = parse_excel(uploaded_file)
        save_students(df)
        flash('File uploaded and data saved successfully!', 'success')
    except ExcelParseError as e:
        flash(str(e), 'error')
        return redirect(url_for('students.upload_page'))
    return redirect(url_for('students.dashboard'))

@students_bp.route("/dashboard")
def dashboard():
    
    students = Student.query.all()
    all_payments = [p for s in students for p in s.payments]
    unpaid_count = sum(1 for p in all_payments if p.status.value != "PAID")
    return render_template("students/dashboard.html", students=students,unpaid_count=unpaid_count)

@students_bp.route("/payments/<int:payment_id>/update", methods=["POST"])#Update the current 
def update_payment(payment_id):
    print("RECEIVED:", payment_id, dict(request.form))
    new_amount = request.form.get("amount_paid")
    try:
        new_amount = float(new_amount)
    except (TypeError, ValueError):
        flash("Enter a valid amount.", "error")
        return redirect(url_for("students.dashboard"))

    mark_payment(payment_id, new_amount)
    flash("Payment updated.", "success")
    return redirect(url_for("students.dashboard"))

@students_bp.route("/payments/<int:payment_id>/remind", methods=["POST"])
def send_reminder(payment_id):
    payment = Payment.query.get(payment_id)
    if payment is None:
        flash("Payment not found.", "error")
        return redirect(url_for("students.dashboard"))

    amount_owed = payment.fee_amount - payment.amount_paid
    message = generate_reminder_message(payment.student.full_name, amount_owed, payment.term)

    flash(f"Reminder for {payment.student.full_name}: {message}", "success")
    return redirect(url_for("students.dashboard"))