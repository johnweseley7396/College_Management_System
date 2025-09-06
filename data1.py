import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import Result, Student

# Define the file path for the results data
results_file_path = r'C:\Users\JOHN WESLEY\OneDrive\Desktop\data\result.xlsx'

# Import results data
results_df = pd.read_excel(results_file_path)

# Clean column names by stripping leading/trailing spaces
results_df.columns = results_df.columns.str.strip()

print(f"Columns found in results file: {results_df.columns.tolist()}")

# Loop through the data and import each row
for index, row in results_df.iterrows():
    # Access the columns and ensure there are no extra spaces
    student_name = str(row['NAME OF THE  STUDENT']).strip()
    email_id = str(row['EMAIL ID']).strip()
    course = str(row['COURSE']).strip()
    roll_number = str(row['ROLL NO']).strip()  # Remove spaces around roll number
    subject = str(row['Subject']).strip()
    semester = str(row['Semester']).strip()
    grade = str(row['Grade']).strip()
    
    # Fetch the student based on the roll number or email (whichever is unique)
    try:
        student = Student.objects.get(roll_number=roll_number)  # Assuming roll number is unique
        # Create a new Result object and associate it with the student
        result_entry = Result(student=student, subject=subject, semester=semester, grade=grade)
        result_entry.save()
    except Student.DoesNotExist:
        print(f"Warning: Student with roll number {roll_number} not found!")

print("✅ Results data import completed.")
