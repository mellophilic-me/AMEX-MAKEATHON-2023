from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import Credit
from .helpers import *
import base64
import face_recognition
import cv2
import numpy as np
from twilio.rest import Client
from django.conf import settings
# Create your views here.

account_sid = settings.ACCOUNT_SID
auth_token = settings.AUTH_TOKEN
verify_sid = settings.VERIFY_SID
cards=Credit.objects.all()
ind=0




client = Client(account_sid, auth_token)
def index(request):
    if request.method=='POST':
        global ind
        global phone_number
        size=len(cards)    
        number=request.POST.get('number')
        name=request.POST.get('holder_name')
        cvc=request.POST.get('cvc')
        month=request.POST.get('month')
        year=request.POST.get('year')
        flag=False
        print("coming in request")
        for i in range(size):
            if(cards[i].Card_num==number and cards[i].holder_name==name and cards[i].cvv==cvc and cards[i].valid_month==month and cards[i].valid_year==year):
                ind=i
                print("working or not ",i)
                
                flag=True
        if flag:
            
            phone_number = cards[ind].mobile
            email = cards[ind].email
            global otp_
            print("Sending the request to phone")
            otp_=send_otp_to_phone(phone_number)
            global otp_e_
            #otp_e_= send_otp_to_email(email)
            return redirect('otpverify')
        else:
            messages.info(request,'Account not found')
            return redirect('creditcard')
    return render(request,'transaction/index.html')
def otp(request):
    if request.method=='POST':
        otp_rec=request.POST.get('m_otp')
        verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=phone_number, code=otp_rec)
        if(otp_!=0 and verification_check.status == "approved"):
            return redirect('face')
        else:
            messages.info(request,'OTP incorrect')
            return redirect('creditcard')
    return render(request,'transaction/otp.html')
def face(request):
    if request.method=='POST':
        print("The index is ",ind)
        img = cards[ind].image
        print(img)
        img = open(str(img),'rb')
        print("breakpoint for image")
        known_image = face_recognition.load_image_file(img)
        cap_img=request.POST.get('captured_image_data')     
        decoded_data=base64.b64decode(cap_img)
        unknown_image = cv2.imdecode(np.frombuffer(decoded_data, np.uint8), -1)
       
        # img_file = open('temp.jpeg', 'wb')
        # img_file.write(decoded_data)
        # img_file.close()
        # unknown_image = face_recognition.load_image_file('temp.jpeg')
        try:
            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces([known_encoding], unknown_encoding)
            print(results)
            if results[0]:
                # img_file2= Image.open('white.jpeg')
                # img_file = img_file2.save('temp.jpeg')
                print("Verification hai")
                
                return redirect('end')
            else:
                # img_file2= Image.open('white.jpeg')
                # img_file = img_file2.save('temp.jpeg')
                messages.info(request,'Verification Unsuccessfull')
                return redirect('creditcard')
        except:
            messages.info(request,'Face Not Captured')
            return redirect('creditcard')
    return render(request,'transaction/face.html')
def first(request):
    return render(request,'transaction/first.html')
def end(request):
    return render(request,'transaction/end.html')