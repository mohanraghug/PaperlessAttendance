from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from ..decorators import admin_required
from attendance.forms import ProfessorSignUpForm,AdminSignUpForm
from ..models import user,Professor,Course,Student,Attendance,Entry
from ..forms import AdminCourseForm,AdminStudentForm,AdminProfessorForm,AdminAttendanceForm,StudentAddForm
class AdminSignUpView(CreateView):
    model = user
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('admin_home')
@method_decorator([login_required, admin_required], name='dispatch')
class StudentListView(ListView):
    model = Student
    ordering = ('Rollno', )
    context_object_name = 'students'
    template_name = 'admin/student_change_list.html'

    def get_queryset(self):
        queryset = Student.objects.all()
        return queryset
@method_decorator([login_required, admin_required], name='dispatch')
class CourseListView(ListView):
    model=Course
    ordering=('Name',)
    context_object_name='courses'
    template_name='admin/course_change_list.html'
    def get_queryset(self):
        queryset=Course.objects.all()
        return queryset
@method_decorator([login_required, admin_required], name='dispatch')
class ProfessorsListView(ListView):
    model=Professor
    ordering=('Name',)
    context_object_name='professors'
    template_name='admin/professor_change_list.html'
    def get_queryset(self):
        queryset=Professor.objects.all()
        return queryset
@method_decorator([login_required, admin_required], name='dispatch')
class AttendanceListView(ListView):
    model=Attendance
    ordering=('Date',)
    context_object_name='attendance'
    template_name='admin/attendance_change_list.html'
    def get_queryset(self):
        queryset=Attendance.objects.all()
        return queryset
@method_decorator([login_required, admin_required], name='dispatch')
class EntriesListView(ListView):
    model=Attendance
    ordering=('Date',)
    context_object_name='entries'
    template_name='admin/entries_change_list.html'
    def get_queryset(self):
        queryset=Entry.objects.all()
        return queryset
@login_required
@admin_required
def course_add(request):
    if request.method=='POST':
        form=AdminCourseForm(request.POST)
        if form.is_valid():
            course=form.save(commit=False)
            course.save()
            messages.success(request,'Added Course Succesfully')
            return redirect('admin_courses')
    else:
        form=AdminCourseForm()
    return render(request,'admin/course_add_form.html',{'form':form})
@login_required
@admin_required
def student_add(request):
    if request.method=='POST':
        form=AdminStudentForm(request.POST,request.FILES)
        if form.is_valid():
            student=Student(Rollno=request.POST['Rollno'],Name=request.POST['Name'],Email=request.POST['Email'],Image=request.FILES['Image'])
            student.save()
            messages.success(request,'Student Added Successfully')
            return redirect('admin_home')
        print(request.POST)
    else:
        form=AdminStudentForm()
    return render(request,'admin/student_add_form.html',{'form':form})
@login_required
@admin_required
def professor_add(request):
    if request.method=='POST':
        form=AdminProfessorForm(request.POST)
        if form.is_valid():
            Prof=form.save(commit=False)
            Prof.save()
            messages.success(request,'Professor Added Successfully')
            return redirect('admin_professors')
    else:
        form=AdminProfessorForm()
    return render(request,'admin/professor_add_form.html',{'form':form})
@login_required
@admin_required
def attendance_add(request):
    if request.method=='POST':
        form=AdminAttendanceForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.save()
            messages.success(request,'attendance entry Added Successfully')
            return redirect('admin_attendance')
    else:
        form=AdminAttendanceForm()
    return render(request,'admin/attendance_add_form.html',{'form':form})
@method_decorator([login_required, admin_required], name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    fields = ('Name','Start_time','end_time','TotalStrength', )
    context_object_name = 'course'
    template_name = 'admin/course_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['students'] = self.get_object().Students.all()
        return super().get_context_data(**kwargs)
    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        
        return Course.objects.all()

    def get_success_url(self):
        return reverse('admin_courses')
@method_decorator([login_required, admin_required], name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'course'
    template_name = 'admin/course_delete_confirm.html'
    success_url = reverse_lazy('admin_courses')

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        messages.success(request, 'The course %s was deleted with success!' % course.Name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Course.objects.all()
@method_decorator([login_required, admin_required], name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    fields = ('Name','Rollno','Email','Image', )
    context_object_name = 'student'
    template_name = 'admin/student_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['courses']=self.get_object().Courses.all()
        return super().get_context_data(**kwargs)
    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        
        return Student.objects.all()

    def get_success_url(self):
        return reverse('admin_home')
@method_decorator([login_required, admin_required], name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    context_object_name = 'student'
    template_name = 'admin/student_delete_confirm.html'
    success_url = reverse_lazy('admin_home')

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        messages.success(request, 'The student %s was deleted with success!' % student.Rollno)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Student.objects.all()
@login_required
@admin_required
def course_add_students(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            rollno=request.POST['Rollno']
            student=Student.objects.get(Rollno=rollno)
            course.Students.add(student)
            messages.success(request, 'Student added Successfully')
            return redirect('admin_course_update', course.pk)
    else:
        form = StudentAddForm()

    return render(request, 'admin/student_add_form.html', {'course': course, 'form': form})

@method_decorator([login_required, admin_required], name='dispatch')
class ProfessorUpdateView(UpdateView):
    model = Professor
    fields = ('Name','Email', )
    context_object_name = 'professor'
    template_name = 'admin/professor_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['courses']=self.get_object().courses.all()
        return super().get_context_data(**kwargs)
    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        
        return Professor.objects.all()
@method_decorator([login_required, admin_required], name='dispatch')
class ProfessorDeleteView(DeleteView):
    model = Professor
    context_object_name = 'professor'
    template_name = 'admin/professor_delete_confirm.html'
    success_url = reverse_lazy('admin_professors')

    def delete(self, request, *args, **kwargs):
        professor= self.get_object()
        messages.success(request, 'The professor %s was deleted with success!' % professor.Name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Professor.objects.all()