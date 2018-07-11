from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from ..decorators import student_required
from attendance.forms import StudentSignupForm
from ..models import  StudentUser,user,Course,Student
class StudentSignUpView(CreateView):
    model = user
    form_class = StudentSignupForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        
        return redirect('student_home')
def unique(a):
    unique=[]
    for x in a:
        if x not in unique:
            unique.append(x)
    return len(unique)
@login_required
@student_required
def CourseListView(request,pk):
    student=Student.objects.get(pk=pk)
    courses=student.Courses.all()
    dictionary={}
    a=[]
    b=[]
    for course in courses:
        for attendance in course.attendance.all():
            a.append(attendance.Date)
        count1=unique(a)
        attendane=Attendance.objects.filter(Student=student,Course=course)
    for course in courses:

        for ar in attendane:
            b.append(ar.Date)
        count2=unique(b)
        dictionary[course.Name]=[count1,count2]
    context={
        'courses':courses,
        'dictionary':dictionary
    }
    return render(request,student/course_change_list.html,context)
    



