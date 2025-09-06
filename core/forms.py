from django import forms
from .models import Staff, Student, Department, Course, Subject
from .models import Attendance


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'department']
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'department']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'department']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'course']

from .models import StudentFeedback

from django import forms
from .models import StudentFeedback

class StudentFeedbackForm(forms.ModelForm):
    class Meta:
        model = StudentFeedback
        fields = ['feedback']
from .models import StaffFeedback

class StaffFeedbackForm(forms.ModelForm):
    class Meta:
        model = StaffFeedback
        fields = ['staff', 'feedback'] 

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'  # Or list specific fields you want users to input