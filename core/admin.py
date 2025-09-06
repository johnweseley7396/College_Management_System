from django.contrib import admin
from .models import Department, Student, Staff, Course, Subject, Attendance, Leave, Result, Fee, StudentFeedback, StaffFeedback

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Result)
admin.site.register(Fee)
admin.site.register(StudentFeedback)
admin.site.register(StaffFeedback)
