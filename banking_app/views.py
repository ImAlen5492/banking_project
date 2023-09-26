import os

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth import logout



# Create your views here.

def register(request):
    if request.method == 'POST':
        a=regform(request.POST,request.FILES)   #(a=regform(fname=alen,lname=raj,email=...)
        if a.is_valid():
            fn=a.cleaned_data['firstname'] #green color is form name
            ln = a.cleaned_data['lastname']
            un = a.cleaned_data['username']
            pn=a.cleaned_data['phone']
            ac=int("15"+str(pn))

            em = a.cleaned_data['email']
            img=a.cleaned_data['image']
            pin = a.cleaned_data['pin']
            cpn = a.cleaned_data['confirmpin']
            if pin==cpn:
                b=regmodel(firstname=fn,lastname=ln,username=un, phone=pn,acnum=ac,email=em, image=img,pin=pin,balance=0)  #orange color is model names
                b.save()
                subject = "your account has been created"
                message = f"your new account number is {ac}"
                email_from = "alanpy20233@gmail.com"
                email_to=em
                send_mail(subject, message, email_from,[email_to])
                return redirect(logregister)
            else:
                return HttpResponse("password doesn't match")
        else:
            return HttpResponse("registration failed")
    return render(request,'registration.html')

def logregister(request):
    if request.method=='POST':
        a=logform(request.POST)
        if a.is_valid():
            fn=a.cleaned_data['username']
            ps=a.cleaned_data['pin']
            b=regmodel.objects.all()
            for i in b:
                if i.pin==ps and i.username==fn:
                    request.session['id']=i.id
                    return redirect(profile)
            else:
                return redirect(logregister)
    return render(request,'login.html')

def index(request):
    return render(request,'index.html')

def profile(request):
    try:
        id1=request.session['id']
        a=regmodel.objects.get(id=id1)
        img=str(a.image).split('/')[-1]
        return render(request,'profile.html',{'a':a,'img':img})
    except:
        return redirect(logregister)


def edit(request,id):
    a=regmodel.objects.get(id=id)
    img = str(a.image).split('/')[-1]
    if request.method=='POST':
        a.firstname=request.POST.get('firstname')
        a.lastname=request.POST.get('lastname')
        a.phone = request.POST.get('phone')
        a.email=request.POST.get('email')
        a.save()
        return redirect(profile)
    return render(request,'edit.html',{'a':a,'img':img})


def editimage(request,id):
    a=regmodel.objects.get(id=id)
    image=str(a.image).split('/')[-1]
    if request.method=='POST':
        a.username=request.POST.get('username')
        if len(request.FILES)!=0:
            if len(a.image)>0:
                os.remove(a.image.path)
            a.image=request.FILES['image']
        a.save()
        return redirect(profile)
    return render(request,'editimage.html',{'a':a,'image':image})

def success(request):
    am=request.session['am']
    ac = request.session['ac']
    return render(request,'success.html',{'am':am,'ac':ac})


def addamoney(request,id):
    x=regmodel.objects.get(id=id)
    if request.method=='POST':
        am=request.POST.get('amount') #withoutform
        pin = request.POST.get('pin')
        request.session['am']=am
        request.session['ac'] = x.acnum
        if pin == x.pin:
            x.balance+=int(am)
            x.save()
            b=addamount(amount=am,uid=request.session['id'])
            b.save()
            return redirect(success)
        else:
            return HttpResponse('amount added failed')

    return render(request,'addamount.html')



def withdrawmoney(request,id):
    x=regmodel.objects.get(id=id)
    if request.method=='POST':
        am = request.POST.get('amount')  # withot form
        request.session['am'] = am
        request.session['ac'] = x.acnum
        pin = request.POST.get('pin')
        if pin == x.pin:
            if(x.balance>=int(am)):
                x.balance -= int(am)
                x.save()
                b=withdrawamount(amount=am,uid=request.session['id'])
                b.save()


                return redirect(withdrawsuccess)
            else:
                return HttpResponse('password incorrect')
        else:
            return HttpResponse('insufficientbalance')

    return render(request,'withdrawamount.html')

def withdrawsuccess(request):
    am=request.session['am']
    ac=request.session['ac']
    return render(request,'withdrawsuccess.html',{'am':am,'ac':ac})

def checkbalance(request,id):
    x = regmodel.objects.get(id=id)
    if request.method == 'POST':
        request.session['balance'] = x.balance
        request.session['ac'] = x.acnum
        pin = request.POST.get('pin')
        if pin == x.pin:
            return redirect(checkbalance1)
        else:
            return HttpResponse(' failed')

    return render(request, 'checkbalance.html')


def checkbalance1(request):
    ac = request.session['ac']
    balance = request.session['balance']
    return render(request, 'checkbalance1.html',{'ac':ac,'balance':balance})


def ministatement(request,id):
    x=regmodel.objects.get(id=id)
    pin=request.POST.get('pin')
    if request.method=='POST':
        if pin== x.pin:
            choice=request.POST.get('statement')
            if choice=='deposit':
                return redirect(deposit)
            elif choice=='withdraw':
                return redirect(withdrawmini)
            else:
                return HttpResponse('password error')
    return render(request,'ministatement.html')

def deposit(request):
    x= addamount.objects.all()
    id=request.session['id']
    return render(request,'depo.html',{'x':x, 'id':id})

def withdrawmini(request):
    x=withdrawamount.objects.all()
    id=request.session['id']
    return render(request,'withmini.html',{'x':x,'id':id})

def news(request):
    if request.method=='POST':
        a=newsform(request.POST,request.FILES)
        if a.is_valid():
            top=a.cleaned_data['topic']
            con=a.cleaned_data['content']
            b=newsmodel(topic=top,content=con)
            b.save()
            return redirect(adminnewsdisplay)
        else:
            return HttpResponse('failed')
    return render(request,'news.html')

def adminlogin(request):
    if request.method=='POST':
        a=adminform(request.POST)
        if a.is_valid():
            us=a.cleaned_data['username']
            ps=a.cleaned_data['password']
            user=authenticate(request,username=us,password=ps)
            if user is not None:
                return redirect(adminprofile)
            else:
                return HttpResponse('failed')
    return render(request,'adminlogin.html')


def adminprofile(request):
    return render(request,'adminprofile.html')

def newsdisplay(request):
    a=newsmodel.objects.all()
    return render(request,'newsdisplay.html',{'a':a})


def adminnewsdisplay(request):
    a=newsmodel.objects.all()
    return render(request,'adminnewsdisplay.html',{'a':a})

def adminnewsdelete(request,id):
    a=newsmodel.objects.get(id=id)
    a.delete()
    return redirect(newsdisplay)


def admineditnews(request,id):
    a=newsmodel.objects.get(id=id)
    if request.method=='POST':
        a.topic=request.POST.get('topic')
        a.content=request.POST.get('content')
        a.save()
        return redirect(adminnewsdisplay)
    return render(request,'admineditnews.html',{'a':a})

def wish(request,id):
    a=newsmodel.objects.get(id=id)
    wish=wishlist.objects.all()
    for i in wish:
        if i.newsid==a.id and i.uid==request.session['id']:
            return HttpResponse('item already in wishlist')
    b=wishlist(topic=a.topic,content=a.content,date=a.date,newsid=a.id,uid=request.session['id'])
    b.save()
    return HttpResponse("ADDED TO WISHLIST")

def wishdisplay(request):
    a=wishlist.objects.all()
    id=request.session['id']
    return render(request,'wishdisplay.html',{'a':a,'id':id})

def logoutview(request):
    logout(request)
    return redirect(index)

def forgot_password(request):
    a=regmodel.objects.all()
    if request.method=='POST':
        em= request.POST.get('email')
        ac= request.POST.get('ac_num')
        for i in a:
            if(i.email==em and i.acnum==int(ac)):

                id=i.id
                subject="Password Change"
                message=f"http://127.0.0.1:8000/banking_app/change/{id}"
                # message="Renew your password"
                frm="alanpy20233@gmail.com"
                to=em
                send_mail(subject,message,frm,[to])
                return HttpResponse("Check Your E-mail")
        else:
            return HttpResponse("Sorry, Some Error Occured")
    return render(request,'forgotpass.html')

def change_password(request,id):
    a=regmodel.objects.get(id=id)
    if request.method=='POST':
        p1=request.POST.get('pin')
        p2=request.POST.get('repin')
        if p1==p2:
            a.pin=p1
            a.save()
            return HttpResponse('Password changed')
        else:
            return HttpResponse('Sorry!!')
    return render(request,'changepass.html')

def moneytransfer(request):
    id1=request.session['id']
    a=regmodel.objects.get(id=id1)
    b=regmodel.objects.all()
    if request.method == 'POST':
        acn = request.POST.get('acname')
        acno = request.POST.get('accntnum')
        am=request.POST.get('amount')
        for i in b:
            if int(i.acnum)==acno and i.username==acn:
                if (a.balance >= int(am)):
                    a.balance-=am
                    a.save()
                    b.balance+=am
                    b.save()
                    return HttpResponse('success')
        else:
            return HttpResponse('wrong')
    return render(request,'moneytransfer.html')