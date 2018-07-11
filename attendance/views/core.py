from django.shortcuts import render
import cognitive_face as CF
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import cv2
from django.http import HttpResponse, HttpResponseNotFound
from attendance.models import Professor,Student,Course,Attendance,Entry
import datetime
import time
import smtplib  as sl
from django.core.mail import send_mail
from django.conf import settings
def sendmail(course):
    subject='Notification regarding Attendance'
    message=f'Your attendance has not been recorded todayfor course {course.Name}.Please contact admin in case of conflicts'
    from_email=settings.EMAIL_HOST_USER
    to_list=['mohanr@iitk.ac.in']
    send_mail(subject,message,from_email,to_list,fail_silently=True)
    return
def send(course,recipints):
    """
    The main body
    """
    username ='mohanr'
    passwd = ''

    # Accepting user input
    _from = 'mohanr@iitk.ac.in'
    send_to = recipints
    cc = ''
    bcc =''
    sub ='fake attendace' 
    #print('\nEnter Message end witth ###: ')
    #sentinel = '###'
    # Accept message terminated by sentinel
    mes = f"""Hi,This is Admin from the attendance section.Your Attendance Entry for today for {course} was
            found to be fake or invalid.Please contact the Attendance Section in the LHC if you think
            this is a mistake.
            Please do not reply.This is a System generated email."""


    print('Success!!')
    print('\nSending from :\n' + _from)
    print('\nSending to :\n' + str(send_to))
    print('\nSending cc :\n' + str(cc))
    print('\nSending bcc :\n' + str(bcc))
    print('\nSubject\n' + sub)
    print('\nMessage :\n' + mes)

    # Only works form inside iitk
    server = sl.SMTP('smtp.cc.iitk.ac.in', 25)
    # For outside, use :
    # server = sl.SMTP('mmtp.iitk.ac.in', 25)

    # Below two lines are required for other servers
    # server.starttls()
    # server.ehlo()
    server.login(username, passwd)

    # Creating Header
    to_send = "To: " + ", ".join(send_to)
    cc_send = "Cc: " + ", ".join(cc)
    from_send = "From: " + _from
    sub_send = "Subject: " + sub
    message = "\r\n".join([from_send, to_send, cc_send, sub_send, '', mes])

    # Sending Mail
    server.sendmail(_from, send_to + cc + bcc, message)
    server.quit()
#A function to compare the first images using face api
def first_image_comparison(img1,img2):
    key = '9c8e1726760945da9917f227f2d2ad5a'  # Replace with a valid Subscription Key here.
    CF.Key.set(key)

    base_url = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
    CF.BaseUrl.set(base_url)

    img_urls = [img1.url,img2.url]

    faces = [CF.face.detect(img_url) for img_url in img_urls]

    # Assume that each URL has at least one face, and that you're comparing the first face in each URL
    # If not, adjust the indices accordingly.
    similarity = CF.face.verify(faces[0][0]['faceId'], faces[1][0]['faceId'])
    return similarity
#A function to compare second image using opencv
def second_image_comparison(img1,img2):
    a = cv2.imread(img1.url)
    b = cv2.imread(img2.url)
    graya = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    grayb = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    re_graya = cv2.resize(graya,(2000,2000))
    re_grayb = cv2.resize(grayb,(2000,2000))
    diff = cv2.absdiff(re_graya,re_grayb)
    nonzero = cv2.countNonZero(diff)
    total1 = a.shape[0] * a.shape[1]
    #total2 = b.shape[0] * b.shape[1]
    #total = total1 + total2
    return ((nonzero*100)/float(total1))


#A function that actually verifies whether attendance is fake or real
def add_attendance(entries):
    b=[]
    n=len(entries)
    failed=[]
    #forming a n*n matrix for secondimage
    for i in range(0,n):
            b.append([])
    #filling the matrix with 0s and 1s
    for i in range(0,n):
        for j in range(0,n):
            if second_image_comparison(entries[i].img2,entries[j].img2)<=50:
                b[i].append(1)
            else:
                b[i].append(0)
    #Checking whether attendance is real or fake
    for i in range(0,n):
        sum=0
        for j in range(0,n):
            sum+=b[i][j]
        if sum>=n//3 and first_image_comparison(entries[i].img1,entries[i].Student.Image)>=0.5:
            a=Attendance(Student=entries[i].Student,Course=entries[i].Course,Date=entries[i].Date)
            a.save()
        else:
            failed.append(entries[i].Student.Email)
    #send mail to those whose attendance is found to be fake
    send(entries[0].Course.Name,failed)
    return

#A function to handle the route to add an attendance entry
@csrf_exempt
def record_attendance(request):
    if request.method=='POST':
        print(request.POST)
        rollno=request.POST['Rollno']
        course=request.POST['Course']
        
        if Student.objects.get(Rollno=rollno) and Course.objects.get(Name=course):
            s=Student.objects.get(Rollno=rollno)
            c=Course.objects.get(Name=course)
            entry=Entry(Student=s,Course=c,img1=request.FILES['img1'],img2=request.FILES['img2'],date=datetime.date.today())
            entry.save()
            return HttpResponse("Recorded the Entry")
        else:
            return HttpResponse("Error")
        
def compute_attendance(request,pk):
    c=Course.objects.get(pk=pk)
    sendmail(c)
    entries=Entry.objects.filter(Course=c,date=datetime.date.today())
    if len(entries)>=2:
        add_attendance(entries)
        return HttpResponse("Computed the Attendance for the course")
    else:
        return HttpResponse('No class today probably')

