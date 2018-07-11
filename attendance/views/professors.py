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
from ..decorators import professor_required
from attendance.forms import ProfessorSignUpForm,StudentAddForm
from ..models import user,Professor,Course,Student

class ProfessorSignUpView(CreateView):
    model = user
    form_class =ProfessorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'professor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('professors_home')
@method_decorator([login_required, professor_required], name='dispatch')
class CourseListView(ListView):
    model = Course
    ordering = ('Name', )
    context_object_name ='courses'
    template_name = 'professors/course_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.professor.courses
            
        return queryset
@method_decorator([login_required, professor_required], name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    fields = ('Name', 'Start_time','end_time','TotalStrength', )
    template_name = 'professors/course_add_form.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.Professor =Professor.objects.get(user=self.request.user) 
        course.save()
        messages.success(self.request, 'The course was created with success! Go ahead and add some students now.')
        return redirect('course_change',course.pk)
@method_decorator([login_required, professor_required], name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    fields = ('Name', 'Start_time','end_time','TotalStrength', )
    context_object_name = 'course'
    template_name = 'professors/course_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['students'] = self.get_object().Students.all()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        
        return Professor.objects.get(user=self.request.user).courses.all()

    def get_success_url(self):
        return reverse('course_change', kwargs={'pk': self.object.pk})
@method_decorator([login_required, professor_required], name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'course'
    template_name = 'professors/course_delete_confirm.html'
    success_url = reverse_lazy('professors_home')

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        messages.success(request, 'The course %s was deleted with success!' % course.Name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Professor.objects.get(user=self.request.user).courses.all()
@login_required
@professor_required
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
            return redirect('course_change', course.pk)
    else:
        form = StudentAddForm()

    return render(request, 'professors/student_add_form.html', {'course': course, 'form': form})
