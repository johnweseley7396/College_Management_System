from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from .models import Student, Result, Fee
import matplotlib.pyplot as plt
import io
import base64
from .models import Department

def home(request):
    return render(request, 'core/home.html')

def student_dashboard_redirect(request):
    roll = request.GET.get('roll')
    if roll:
        return redirect(f'/student-dashboard/{roll}/')
    return redirect('/')


def check_result(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        semester = request.POST.get('semester')

        try:
            student = Student.objects.get(roll_number=roll_number)

            # Eliminate duplicates: get one result per subject
            all_results = Result.objects.filter(student=student, semester=semester).order_by('subject', 'id')
            unique_results = []
            seen_subjects = set()

            for result in all_results:
                if result.subject not in seen_subjects:
                    unique_results.append(result)
                    seen_subjects.add(result.subject)

            return render(request, 'core/check_result.html', {
                'student': student,
                'result': unique_results,
                'semester': semester
            })

        except Student.DoesNotExist:
            return HttpResponse("<h1>Student not found</h1>")

    return render(request, 'core/check_result_form.html')



def check_fee(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        try:
            student = Student.objects.get(roll_number=roll_number)
            fee_status = Fee.objects.filter(student=student).last()
            if fee_status:
                return render(request, 'core/check_fee.html', {
                    'student': student,
                    'fee_status': fee_status,
                })
            else:
                return HttpResponse("<h1>No fee records found for this student.</h1>")
        except Student.DoesNotExist:
            return HttpResponse("<h1>Student not found</h1>")
    return render(request, 'core/check_fee_form.html')


from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Student, Result, Fee
import matplotlib.pyplot as plt
import io
import base64

def student_dashboard(request, roll_number):
    student = get_object_or_404(Student, roll_number=roll_number)

    # Remove duplicates by subject (same logic)
    all_results = Result.objects.filter(student=student).order_by('semester', 'subject', 'id')
    results = []
    seen_subjects = set()

    for result in all_results:
        key = (result.semester, result.subject)  # Ensures uniqueness across both
        if key not in seen_subjects:
            results.append(result)
            seen_subjects.add(key)

    # Fee logic remains unchanged
    latest_fee = Fee.objects.filter(student=student).last()
    fees = [latest_fee] if latest_fee else []
    total_fee_paid = latest_fee.amount_paid if latest_fee else 0
    total_fee_due = latest_fee.due_amount if latest_fee else 0

    # Grade distribution
    grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
    for result in results:
        if result.grade in grade_count:
            grade_count[result.grade] += 1

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(grade_count.values(), labels=grade_count.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    return render(request, 'core/student_dashboard.html', {
        'student': student,
        'results': results,
        'fees': fees,
        'total_fee_paid': total_fee_paid,
        'total_fee_due': total_fee_due,
        'grade_count': grade_count,
        'img_base64': img_base64,
    })


def admin_dashboard(request):
    total_students = Student.objects.count()
    total_results = Result.objects.count()
    total_fee_paid = Fee.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_fee_due = Fee.objects.aggregate(Sum('due_amount'))['due_amount__sum'] or 0

    grade_counts = {
        'A': Result.objects.filter(grade='A').count(),
        'B': Result.objects.filter(grade='B').count(),
        'C': Result.objects.filter(grade='C').count(),
        'F': Result.objects.filter(grade='F').count(),
    }

    return render(request, 'core/admin_dashboard.html', {
        'total_students': total_students,
        'total_results': total_results,
        'total_fee_paid': total_fee_paid,
        'total_fee_due': total_fee_due,
        'grade_counts': grade_counts,
    })

from django.shortcuts import render
from .models import Department  # make sure you have imported Department

def hod_dashboard(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'core/hod_dashboard.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff
from .forms import StaffForm

def manage_staff(request):
    staffs = Staff.objects.all()
    return render(request, 'core/manage_staff.html', {'staffs': staffs})

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_staff')
    else:
        form = StaffForm()
    return render(request, 'core/add_staff.html', {'form': form})

def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('manage_staff')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'core/edit_staff.html', {'form': form})

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.delete()
        return redirect('manage_staff')
    return render(request, 'core/delete_staff.html', {'staff': staff})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

# 1. List all students (manage_student)
def manage_student(request):
    students = Student.objects.all()
    return render(request, 'core/manage_student.html', {'students': students})

# 2. Add a new student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_student')
    else:
        form = StudentForm()
    return render(request, 'core/add_student.html', {'form': form})

# 3. Edit an existing student
def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('manage_student')
    else:
        form = StudentForm(instance=student)
    return render(request, 'core/edit_student.html', {'form': form})

# 4. Delete a student
def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('manage_student')
    return render(request, 'core/delete_student.html', {'student': student})
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from .models import Student, Staff, Course, Subject, Attendance, StudentFeedback, StaffFeedback, Fee, Result, Department
from .forms import StudentForm, StaffForm, CourseForm, SubjectForm, StudentFeedbackForm, StaffFeedbackForm

# Home and Dashboards
def home(request):
    return render(request, 'core/home.html')

def admin_dashboard(request):
    total_students = Student.objects.count()
    total_results = Result.objects.count()
    total_fee_paid = Fee.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_fee_due = Fee.objects.aggregate(Sum('due_amount'))['due_amount__sum'] or 0

    grade_counts = {
        'A': Result.objects.filter(grade='A').count(),
        'B': Result.objects.filter(grade='B').count(),
        'C': Result.objects.filter(grade='C').count(),
        'F': Result.objects.filter(grade='F').count(),
    }

    return render(request, 'core/admin_dashboard.html', {
        'total_students': total_students,
        'total_results': total_results,
        'total_fee_paid': total_fee_paid,
        'total_fee_due': total_fee_due,
        'grade_counts': grade_counts,
    })

def hod_dashboard(request):
    departments = Department.objects.all()
    return render(request, 'core/hod_dashboard.html', {'departments': departments})

# Student CRUD
def manage_student(request):
    students = Student.objects.all()
    return render(request, 'core/manage_student.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_student')
    else:
        form = StudentForm()
    return render(request, 'core/add_student.html', {'form': form})

def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('manage_student')
    else:
        form = StudentForm(instance=student)
    return render(request, 'core/edit_student.html', {'form': form})

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('manage_student')
    return render(request, 'core/delete_student.html', {'student': student})

# Staff CRUD
def manage_staff(request):
    staffs = Staff.objects.all()
    return render(request, 'core/manage_staff.html', {'staffs': staffs})

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_staff')
    else:
        form = StaffForm()
    return render(request, 'core/add_staff.html', {'form': form})

def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('manage_staff')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'core/edit_staff.html', {'form': form})

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.delete()
        return redirect('manage_staff')
    return render(request, 'core/delete_staff.html', {'staff': staff})

# Course CRUD
def manage_course(request):
    courses = Course.objects.all()
    return render(request, 'core/manage_course.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_course')
    else:
        form = CourseForm()
    return render(request, 'core/add_course.html', {'form': form})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('manage_course')
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/edit_course.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('manage_course')
    return render(request, 'core/delete_course.html', {'course': course})

# Subject CRUD
def manage_subject(request):
    subjects = Subject.objects.all()
    return render(request, 'core/manage_subject.html', {'subjects': subjects})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_subject')
    else:
        form = SubjectForm()
    return render(request, 'core/add_subject.html', {'form': form})

def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('manage_subject')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'core/edit_subject.html', {'form': form})

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        return redirect('manage_subject')
    return render(request, 'core/delete_subject.html', {'subject': subject})

# View Attendance
def view_attendance(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'core/view_attendance.html', {'attendance_records': attendance_records})

# Feedback
def student_feedback(request):
    if request.method == 'POST':
        form = StudentFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_feedback')
    else:
        form = StudentFeedbackForm()
    return render(request, 'core/student_feedback.html', {'form': form})

def staff_feedback(request):
    if request.method == 'POST':
        form = StaffFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_feedback')
    else:
        form = StaffFeedbackForm()
    return render(request, 'core/staff_feedback.html', {'form': form})



#feedback curd operation
from django.shortcuts import render, redirect, get_object_or_404
from .models import StaffFeedback
from .forms import StaffFeedbackForm  # We'll assume you created this form
from django.contrib import messages

def manage_feedback(request):
    feedbacks = StaffFeedback.objects.all().order_by('-date_submitted')
    context = {'feedbacks': feedbacks}
    return render(request, 'core/manage_feedback.html', context)

def add_feedback(request):
    if request.method == 'POST':
        form = StaffFeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback added successfully.")
            return redirect('manage_feedback')
    else:
        form = StaffFeedbackForm()
    return render(request, 'core/add_feedback.html', {'form': form})

def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(StaffFeedback, id=feedback_id)
    if request.method == 'POST':
        form = StaffFeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback updated successfully.")
            return redirect('manage_feedback')
    else:
        form = StaffFeedbackForm(instance=feedback)
    return render(request, 'core/edit_feedback.html', {'form': form})

def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(StaffFeedback, id=feedback_id)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, "Feedback deleted successfully.")
        return redirect('manage_feedback')
    # You can confirm deletion on GET request
    return render(request, 'core/delete_feedback_confirm.html', {'feedback': feedback})



#attendance curd operations
from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance  # Assuming you have an Attendance model
from .forms import AttendanceForm  # Assuming you have an AttendanceForm form
from django.contrib import messages

def manage_attendance(request):
    attendances = Attendance.objects.all().order_by('-date')  # Assuming Attendance has a 'date' field
    context = {'attendances': attendances}
    return render(request, 'core/manage_attendance.html', context)

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance added successfully.")
            return redirect('manage_attendance')
    else:
        form = AttendanceForm()
    return render(request, 'core/add_attendance.html', {'form': form})

def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect('manage_attendance')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'core/edit_attendance.html', {'form': form})

def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect('manage_attendance')
    # Confirm delete page on GET
    return render(request, 'core/delete_attendance_confirm.html', {'attendance': attendance})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Staff, Student, Department, Attendance, Leave, Subject, Result, StudentFeedback, StaffFeedback

# 1. Staff Dashboard View
def staff_dashboard(request):
    staff = Staff.objects.first()  # Replace with actual logged-in staff in real scenario

    department_obj = staff.department
    total_students_under_me = Student.objects.filter(department=department_obj).count()
    total_attendance_taken = Attendance.objects.filter(subject__staff=staff).count()
    total_leave_taken = Leave.objects.filter(staff=staff).count()
    total_subjects = Subject.objects.filter(staff=staff).count()

    leave_approved = Leave.objects.filter(staff=staff, status='Approved').count()
    leave_pending = Leave.objects.filter(staff=staff, status='Pending').count()
    leave_rejected = Leave.objects.filter(staff=staff, status='Rejected').count()

    subjects = Subject.objects.filter(staff=staff)
    subject_attendance_counts = [
        {'subject': sub.name, 'count': Attendance.objects.filter(subject=sub).count()} for sub in subjects
    ]

    attendance_records = Attendance.objects.filter(subject__staff=staff).order_by('-date')[:10]

    context = {
        'total_students_under_me': total_students_under_me,
        'total_attendance_taken': total_attendance_taken,
        'total_leave_taken': total_leave_taken,
        'total_subjects': total_subjects,
        'leave_approved': leave_approved,
        'leave_pending': leave_pending,
        'leave_rejected': leave_rejected,
        'subject_attendance_counts': subject_attendance_counts,
        'attendance_records': attendance_records,
    }

    return render(request, 'core/staff_dashboard.html', context)

# from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Staff, Subject, Student, Attendance

def take_attendance(request):
    staff = Staff.objects.first()  # Using the first staff record temporarily (since no login)

    if not staff:
        messages.error(request, "No staff record found.")
        return redirect('staff_home')  # Or any valid URL name

    subjects = Subject.objects.filter(staff=staff)  # Subjects handled by this staff
    students = Student.objects.filter(department__name=staff.department)  # Matching department name

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        subject = get_object_or_404(Subject, id=subject_id)
        date = timezone.now().date()

        for student in students:
            status = request.POST.get(f'status_{student.id}')
            Attendance.objects.create(
                student=student,
                subject=subject,
                date=date,
                status=status
            )

        messages.success(request, "Attendance submitted successfully!")
        return redirect('take_attendance')

    context = {
        'subjects': subjects,
        'students': students,
    }
    return render(request, 'core/take_attendance.html', context)


# 3. View/Update Attendance View
def view_update_attendance(request):
    staff = Staff.objects.first()
    attendances = Attendance.objects.filter(subject__staff=staff).order_by('-date')

    if request.method == 'POST':
        attendance_id = request.POST.get('attendance_id')
        new_status = request.POST.get('status')

        attendance = get_object_or_404(Attendance, id=attendance_id)
        attendance.status = new_status
        attendance.save()

        messages.success(request, "Attendance updated successfully!")
        return redirect('update_attendance')

    return render(request, 'core/view_update_attendance.html', {'attendances': attendances})

# 4. Add Result View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Staff, Student, Subject, Result

def add_result(request):
    staff = Staff.objects.first()  # In real app: request.user.staff
    subjects = Subject.objects.filter(staff=staff)
    students = Student.objects.filter(department=staff.department)

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')
        marks = request.POST.get('marks')

        subject = get_object_or_404(Subject, id=subject_id)
        student = get_object_or_404(Student, id=student_id)

        Result.objects.create(student=student, subject=subject, marks=marks)
        messages.success(request, "Result added successfully!")
        return redirect('add_result')

    # 💡 Correct foreign key lookup
    results = Result.objects.filter(subject__staff=staff).order_by('-date_added')[:5]

    return render(request, 'core/add_result.html', {
        'subjects': subjects,
        'students': students,
        'results': results
    })


# 5. Apply Leave View
def apply_leave(request):
    staff = Staff.objects.first()

    if request.method == 'POST':
        reason = request.POST.get('reason')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        Leave.objects.create(
            staff=staff,
            reason=reason,
            from_date=from_date,
            to_date=to_date,
            status='Pending'
        )
        messages.success(request, "Leave request submitted!")
        return redirect('apply_leave')

    return render(request, 'core/apply_leave.html')

# 6. Feedback View
def feedback(request):
    staff = Staff.objects.first()

    if request.method == 'POST':
        message = request.POST.get('message')
        StaffFeedback.objects.create(staff=staff, message=message)
        messages.success(request, "Feedback submitted successfully!")
        return redirect('staff_feedback')

    return render(request, 'core/feedback.html')

# 7. Staff Home View
def staff_home(request):
    return render(request, 'core/staff_home.html')

# 8. Students Under Me View
def students_under_me(request):
    staff = Staff.objects.first()
    students = Student.objects.filter(department=staff.department)
    return render(request, 'core/students_under_me.html', {'students': students})

# 9. Attendance Details View
def attendance_details(request):
    staff = Staff.objects.first()
    attendances = Attendance.objects.filter(subject__staff=staff).order_by('-date')
    return render(request, 'core/attendance_details.html', {'attendances': attendances})

# 10. Leave Details View
def leave_details(request):
    staff = Staff.objects.first()
    leaves = Leave.objects.filter(staff=staff).order_by('-from_date')
    return render(request, 'core/leave_details.html', {'leaves': leaves})

# 11. Subject List View
def subject_list(request):
    staff = Staff.objects.first()
    subjects = Subject.objects.filter(staff=staff)
    return render(request, 'core/subject_list.html', {'subjects': subjects})



from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Fee

def dummy_payment(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)

    # Simulate payment
    fee.amount_paid = fee.total_amount
    fee.due_amount = 0
    fee.is_paid = True
    fee.payment_date = timezone.now()
    fee.save()

    return redirect('fee_receipt', fee_id=fee.id)

def fee_receipt(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)
    return render(request, 'core/fee_receipt.html', {'fee': fee})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Student, Fee

def pay_fee_by_roll(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        amount_paid = float(request.POST.get('amount_paid'))

        try:
            student = Student.objects.get(roll_number=roll_number)
            fee = Fee.objects.filter(student=student).first()  # Use first() to avoid MultipleObjectsReturned

            if fee is None:
                messages.error(request, "Fee record not found for this student!")
                return redirect('pay_fee_by_roll')

            if amount_paid > fee.due_amount:
                messages.error(request, "You cannot pay more than the due amount.")
                return redirect('pay_fee_by_roll')

            fee.amount_paid += amount_paid
            fee.due_amount -= amount_paid
            fee.is_paid = fee.due_amount == 0
            fee.payment_date = timezone.now()
            fee.save()

            return redirect('fee_receipt_by_roll', roll_number=roll_number)

        except Student.DoesNotExist:
            messages.error(request, "Invalid Roll Number!")

    return render(request, 'core/pay_fee_by_roll.html')


def fee_receipt_by_roll(request, roll_number):
    student = get_object_or_404(Student, roll_number=roll_number)
    fee = Fee.objects.filter(student=student).first()
    return render(request, 'core/fee_receipt_by_roll.html', {'fee': fee, 'student': student})
from django.shortcuts import render, redirect
from django.http import HttpResponse

def custom_admin_login(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Hardcoded username and password for admin login
        if username == 'myadmin' and password == 'mypassword123':
            return redirect('/admin/')  # Redirect to Django Admin Panel if credentials match
        else:
            error = "Invalid username or password"

    return render(request, 'custom_admin_login.html', {'error': error})
