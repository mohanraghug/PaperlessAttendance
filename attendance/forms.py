from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from attendance.models import user,Professor,Student,Course,Attendance,Entry,StudentUser
class ProfessorSignUpForm(UserCreationForm):
    Email=forms.EmailField()
    Name=forms.CharField(max_length=64)
    class Meta(UserCreationForm.Meta):
        model = user
        fields=('Name','Email','username','password1','password2')
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_professor = True
        user.save()
        Prof = Professor.objects.create(user=user,Name=self.cleaned_data.get('Name'),Email=self.cleaned_data.get('Email'))
        return user
class StudentSignupForm(UserCreationForm):
    Rollno=forms.IntegerField()
    class Meta(UserCreationForm.Meta):
        model=user
        
        fields=('Rollno','username','password1','password2')
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student=Student.objects.get(Rollno=self.cleaned_data.get('Rollno'))
        studentuser=StudentUser.objects.create(user=user,Student=student)
        return user
class AdminSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=user
    @transaction.atomic
    def save(self):
        user=super().save(commit=False)
        user.is_admin=True
        user.save()
        return user
class AdminCourseForm(forms.ModelForm):
    Professor=forms.ModelChoiceField(queryset=Professor.objects.all(),widget=forms.RadioSelect(),required=True,empty_label=None)
    class Meta:
        model=Course
        fields=('Name','Professor','Start_time','end_time','TotalStrength')
class AdminStudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=('Name','Rollno','Email','Image')
class AdminProfessorForm(forms.ModelForm):
    class Meta:
        model=Professor
        fields=('Name','Email')
class AdminAttendanceForm(forms.ModelForm):
    Student=forms.ModelChoiceField(queryset=Student.objects.all(),widget=forms.RadioSelect(),required=True,empty_label=None)
    Course=forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.RadioSelect(),required=True,empty_label=None)
    Date=forms.DateInput()
    class Meta:
        model=Attendance
        fields=('Student','Course','Date',)
class StudentAddForm(forms.ModelForm):
    Rollno=forms.IntegerField()
    class Meta:
        model=Student
        fields=('Rollno',)
        