import pandas as pd
from app.extensions import db
from app.models.model import Student,Payment,PaymentStatus
REQUIRED_COLUMNS = {
    "Full Name",
    "Admission Number",
    "Class",
    "Guardian Name",
    "Guardian Phone",
    "Term",
    "Fee Amount",
    "Amount Paid",
    "Payment Date"
}

class ExcelParseError(Exception):
    pass

def parse_excel(file_storage):
   try:#Read the excel file#This function is used to read and extract data from the excel file
       df = pd.read_excel(file_storage)
   except Exception as e:#If reading fails raise an error
       raise ExcelParseError(f"Failed to read the excel file : {e}") from e
   missing_columns = REQUIRED_COLUMNS - set(df.columns)
   if missing_columns:
       raise ExcelParseError(f"Missing required column(s): {missing_columns}") 
   if df.empty:
       raise ExcelParseError("The uploaded file has no data rows.")
   return df 
# Next we are going to wrap this in error handling

def save_students(df):
    if df is None:
        raise ValueError("A dataframe is required to save students.")
    for index, row in df.iterrows():
        # saving logic should be implemented here
        student = Student.query.filter_by(admission_number=row["Admission Number"]).first()

        if student is None:
            student = Student(
                 admission_number=row["Admission Number"],
                full_name=row["Full Name"],
                student_class=row["Class"],
                guardian_name=row["Guardian Name"],
                guardian_phone=None if pd.isna(row["Guardian Phone"]) else row["Guardian Phone"],
            )
            db.session.add(student)
    

        payment = Payment.query.filter_by(student_id=student.id, term=row["Term"]).first()

        if payment is None:
         payment = Payment(
            student=student,
            term=row["Term"],
            fee_amount= row["Fee Amount"],
            amount_paid = row["Amount Paid"],
            payment_date =None if pd.isna(row["Payment Date"]) else pd.to_datetime(row["Payment Date"]).date()
         )
         db.session.add(payment)
        else:
         payment.amount_paid = row["Amount Paid"]
         payment.payment_date = None if pd.isna(row["Payment Date"]) else pd.to_datetime(row["Payment Date"]).date()

        payment.recalculate_status()
    db.session.commit()#One atomic commit to save all the changes to the database at once, ensuring data integrity and consistency.
    

def mark_payment(payment_id, new_amount_paid):
   payment = Payment.query.get(payment_id)
   if payment is None:
      raise ValueError("Payment not found.")
   payment.amount_paid = new_amount_paid #Update the current amount with the new amount entered by the user
   payment.recalculate_status()#Recalculate the new status value based on the input
   db.session.commit()
   return payment

