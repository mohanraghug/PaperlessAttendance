from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from attendance.models import StudentUser,Student
class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_professor:
            return redirect('professors_home')
        elif request.user.is_admin:
            return redirect('admin_home')
        else:
            studentuser=StudentUser.objects.get(user=request.user)
            student=studentuser.Student
            return redirect('student_home',student.id)
    return render(request, 'home.html')

