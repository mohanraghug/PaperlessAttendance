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
        user = form.save()
        login(self.request, user)
        return redirect('student_home')
@method_decorator([login_required, student_required], name='dispatch')
class CourseListView(ListView):
    model=Course
    ordering=('Name',)
    context_object_name='courses'
    template_name='student/student_course_list.html'
    def get_queryset(self):
        student=StudentUser.objects.get(user=self.request.user).Student
        queryset=student.Courses.all()
        return queryset


