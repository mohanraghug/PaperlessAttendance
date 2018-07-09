from django.db import models
from django.utils.html import escape, mark_safe
from django.contrib.auth.models import AbstractUser
# Create your models here.

class user(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_professor= models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

class Professor(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True,related_name='professor')
    Name=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100,unique=True)
    def __str__(self):
        return f"{self.Name}"
class Student(models.Model):
    #user = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True)
    Name=models.CharField(max_length=200)
    Rollno=models.CharField(max_length=10)
    Email=models.EmailField(max_length=100,unique=True)
    Image=models.ImageField(upload_to='images/student/')
    
    def __str__(self):
        return f"{self.Rollno}"
class Course(models.Model):
    Name=models.CharField(max_length=10,unique=True,null=False)
    Professor=models.ForeignKey(Professor,on_delete=models.CASCADE,related_name='courses')
    Start_time=models.TimeField(max_length=200,default='')
    end_time=models.TimeField(max_length=200,default='')
    TotalStrength=models.IntegerField(default=0)
    Students=models.ManyToManyField('Student',related_name='Courses')
    def __str__(self):
        return f"{self.Name}"
class Entry(models.Model):
    Student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='entries')
    Course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='entries')
    img1=models.ImageField(upload_to="entries/image1/")
    img2=models.ImageField(upload_to="entries/image2/")
    date=models.DateField()
    def __str__(self):
        return f"{self.Student.Rollno}-{self.Course.Name}-{self.date}"
class Attendance(models.Model):
    Student=models.ForeignKey('Student',on_delete=models.CASCADE,related_name="attendance")
    Course=models.ForeignKey('Course',on_delete=models.CASCADE,related_name="attendance")
    Date=models.DateField()
class StudentUser(models.Model):
    user=models.OneToOneField(user,on_delete=models.CASCADE,primary_key=True)
    Student=models.OneToOneField(Student,on_delete=models.CASCADE)
