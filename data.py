import os
import django
import pandas as pd

# Step 1: Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

# Step 2: Import models after setting up Django
from core.models import Student

# Step 3: Load Excel file
file_path =r'C:\Users\JOHN WESLEY\OneDrive\Desktop\data\student.xlsx'# Ensure this path is correct
df = pd.read_excel(file_path)
df.columns = df.columns.str.replace(" ", "").str.strip()
print("Columns found in Excel file:")
print(df.columns.tolist())

# Step 4: Iterate through Excel and insert into database
for index, row in df.iterrows():
    roll_number = str(row['ROLL_NO']).strip()
    name = str(row['NAME_OF_THE_STUDENT']).strip()
    email = str(row['EMAIL_ID']).strip()
    course = str(row['COURSE']).strip()

    # Check if student already exists to prevent duplicates
    if not Student.objects.filter(roll_number=roll_number).exists():
        Student.objects.create(
            roll_number=roll_number,
            name=name,
            email=email,
            course=course
        )

print("✅ Student data import completed.")
