from app.extensions import db
from datetime import datetime
import enum
class Student(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    admission_number = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(120),nullable=False)
    student_class = db.Column(db.String(20), nullable =False)
    guardian_name = db.Column(db.String(120), nullable=False)
    guardian_phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payments = db.relationship('Payment', back_populates="student",cascade="all,delete-orphan")#A 1 -->M relationship between  the Student and the payment table

class PaymentStatus(enum.Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"

class Payment(db.Model):
    id =db.Column(db.Integer(),primary_key=True)
    student_id = db.Column(db.Integer(),db.ForeignKey('student.id'),nullable=False)
    term = db.Column(db.String(30), nullable=False)
    fee_amount = db.Column(db.Numeric(10,0), nullable=False)
    amount_paid = db.Column(db.Numeric(10,0), nullable=False, default=0)
    payment_date = db.Column(db.Date,nullable=True)
    status = db.Column(db.Enum(PaymentStatus),nullable=False,default=PaymentStatus.UNPAID)
    student = db.relationship('Student',back_populates="payments")#A M --> 1 relationship between the payment and the student table

    def recalculate_status(self):
        if self.amount_paid <= 0:
            self.status = PaymentStatus.UNPAID
        elif self.amount_paid < self.fee_amount:
            self.status = PaymentStatus.PARTIALLY_PAID
        else:
            self.status = PaymentStatus.PAID
