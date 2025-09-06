from django.db import models

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    hod_name = models.CharField(max_length=100)
    total_students = models.IntegerField()
    total_staffs = models.IntegerField()
    total_courses = models.IntegerField()
    total_subjects = models.IntegerField()

    def __str__(self):
        return self.name

# Student Model
class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.name:
            return self.name
        return self.email

# Result Model
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.student.name} - {self.subject} ({self.semester}) - Grade: {self.grade}'

# Fee Model
# models.py

from django.db import models
from .models import Student  # Ensure you import your Student model

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    email_id = models.EmailField()
    course = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    due_amount = models.FloatField(verbose_name="Due Amount")
    amount_paid = models.FloatField(verbose_name="Amount Paid")
    total_amount = models.FloatField(verbose_name="Total Amount")
    is_paid = models.BooleanField(default=False)  # Payment status
    payment_date = models.DateTimeField(null=True, blank=True)  # When payment was done
    created_at = models.DateTimeField(auto_now_add=True)  # NEW: To track when this record was added
    updated_at = models.DateTimeField(auto_now=True)      # NEW: To track when this record was last updated

    def __str__(self):
        return f"{self.student.name} - ₹{self.amount_paid} paid"

    class Meta:
        get_latest_by = 'created_at'  # Allows use of .latest('created_at') to fetch the latest fee record

# Staff Model
class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)  # Not a ForeignKey
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

# Attendance Model
class Attendance(models.Model):
    ATTENDANCE_STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date} : {self.status}"

# Leave Model
class Leave(models.Model):
    LEAVE_STATUS = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.DateField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS)

    def __str__(self):
        return f"{self.staff} - {self.leave_date} : {self.status}"

# Student Feedback Model
class StudentFeedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.student} on {self.date_submitted.strftime('%Y-%m-%d')}"

# Staff Feedback Model
class StaffFeedback(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.staff} on {self.date_submitted.strftime('%Y-%m-%d')}"
