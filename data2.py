import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

# Import models
from core.models import Fee, Student

# Read the Excel file
df = pd.read_excel(r'C:\Users\JOHN WESLEY\OneDrive\Desktop\data\fees.xlsx')

# Debug: Print column names to ensure correct cleaning
print("Original Columns:", df.columns)

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "").str.replace("₹", "").str.replace("(", "").str.replace(")", "")

# Debug: Print cleaned column names
print("Cleaned Columns:", df.columns)

# Ensure numeric conversion (handle invalid rows gracefully)
df['DueAmount'] = pd.to_numeric(df['DueAmount'], errors='coerce')
df['AmountPaid'] = pd.to_numeric(df['AmountPaid'], errors='coerce')
df['TotalAmount'] = pd.to_numeric(df['TotalAmount'], errors='coerce')

# Check the first few rows of the dataframe to confirm data
print(df.head())

# Loop to save fee data
for index, row in df.iterrows():
    try:
        # Debug: Print row for each iteration to see which data is being processed
        print(f"Processing: {row['ROLLNO']}, {row['DueAmount']}, {row['AmountPaid']}, {row['TotalAmount']}")
        
        student = Student.objects.get(roll_number=row['ROLLNO'])
        fee = Fee(
            student=student,
            due_amount=row['DueAmount'],
            amount_paid=row['AmountPaid'],
            total_amount=row['TotalAmount']
        )
        fee.save()
        print(f"✅ Saved fee for: {student.name} - {student.roll_number}")
    except Student.DoesNotExist:
        print(f"❌ Student with roll number {row['ROLLNO']} not found.")
    except Exception as e:
        print(f"❌ Error with roll number {row['ROLLNO']}: {e}")
