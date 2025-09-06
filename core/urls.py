from django.urls import path
from . import views

# Uncomment this if you want to use namespacing in templates
# app_name = 'core'   

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('hod-dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # Student Dashboard redirect (for roll number input form)
    path('student-dashboard-redirect/', views.student_dashboard_redirect, name='student_dashboard_redirect'),

    # Student Dashboard by roll number
    path('student-dashboard/<str:roll_number>/', views.student_dashboard, name='student_dashboard'),

    # Result checking form & display
    path('check-result/', views.check_result, name='check_result'),
    path('pay-fee-by-roll/', views.pay_fee_by_roll, name='pay_fee_by_roll'),
    path('fee-receipt-by-roll/<str:roll_number>/', views.fee_receipt_by_roll, name='fee_receipt_by_roll'),

    # Fee checking form & display
    path('check-fee/', views.check_fee, name='check_fee'),

    # Fee Payment and Receipt
    path('pay-fee/<int:fee_id>/', views.dummy_payment, name='dummy_payment'),
    path('fee-receipt/<int:fee_id>/', views.fee_receipt, name='fee_receipt'),

    # Student CRUD
    path('manage-student/', views.manage_student, name='manage_student'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

    # Staff CRUD
    path('manage-staff/', views.manage_staff, name='manage_staff'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('edit-staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete-staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    # Course CRUD
    path('manage-course/', views.manage_course, name='manage_course'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),

    # Subject CRUD
    path('manage-subject/', views.manage_subject, name='manage_subject'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    # Attendance CRUD
    path('manage-attendance/', views.manage_attendance, name='manage_attendance'),
    path('add-attendance/', views.add_attendance, name='add_attendance'),
    path('edit-attendance/<int:attendance_id>/', views.edit_attendance, name='edit_attendance'),
    path('delete-attendance/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),

    # Feedback CRUD (Staff Feedback)
    path('manage-feedback/', views.manage_feedback, name='manage_feedback'),
    path('add-feedback/', views.add_feedback, name='add_feedback'),
    path('edit-feedback/<int:feedback_id>/', views.edit_feedback, name='edit_feedback'),
    path('delete-feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

    # Feedback forms for students and staff
    path('student-feedback/', views.student_feedback, name='student_feedback'),
    path('staff-feedback/', views.staff_feedback, name='staff_feedback'),

    # View attendance records (read-only)
    path('view-attendance/', views.view_attendance, name='view_attendance'),

   path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('take-attendance/', views.take_attendance, name='take_attendance'),
    path('view-update-attendance/', views.view_update_attendance, name='update_attendance'),
    path('add-result/', views.add_result, name='add_result'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('feedback/', views.feedback, name='staff_feedback'),
    path('staff-home/', views.staff_home, name='staff_home'),

    # Newly added:
    path('students-under-me/', views.students_under_me, name='students_under_me'),
    path('attendance-details/', views.attendance_details, name='attendance_details'),
    path('leave-details/', views.leave_details, name='leave_details'),
    path('subject-list/', views.subject_list, name='subject_list'),

 #admin login
 path('admin-login/', views.custom_admin_login, name='custom_admin_login'),
]

