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
from ..models import  StudentUser,user,Course,Student,Attendance
class StudentSignUpView(CreateView):
    model = user
    form_class = StudentSignupForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        studentuser=StudentUser.objects.get(user=user)
        s=studentuser.Student
        return redirect('student_home',s.id)
def unique(a):
    unique=[]
    for x in a:
        if x not in unique:
            unique.append(x)
    return len(unique)
class temp:
    def __init__(self,Name,count1,count2):
        self.Name=Name
        self.count1=count1
        self.count2=count2
@login_required
@student_required
def CourseListView(request,pk):
    #studentuser=StudentUser.objects.get(Student=)
    student=Student(pk=pk)
    courses=student.Courses.all()
    temp1=[]
    #context={}
    a=[]
    b=[]
    for course in courses:
        for attendance in course.attendance.all():
            a.append(attendance.Date)
        count1=unique(a)
    
    for course in courses:
        attendane=Attendance.objects.filter(Student=student,Course=course)
        for ar in attendane:
            b.append(ar.Date)
        count2=unique(b)
        new=temp(Name=course.Name,count1=count1,count2=count2)
        temp1.append(new)
    context={
        'courses':temp1
    }
    
    return render(request,'student/course_change_list.html',context)
    



