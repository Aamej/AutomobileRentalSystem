from adminapp.views import bookings
from django.shortcuts import render,redirect
from carapp.models import Customers,Users,CarVariant,Category,JourneyStage,Feedback,Drivers,Payment,Bookings,Car
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator

# Create your views here.
def homepage(req):
    cars=CarVariant.objects.all()
    return render(req,"index.html",locals())

def contactus(req):
    return render(req,"contact.html")


def aboutus(req):
    return render(req,"about-us.html")


def registerpage(req):
    if(req.method=="POST"):
        userid=req.POST.get("userid")
        uname=req.POST.get("uname")
        pwd=req.POST.get("pwd")
        gender=req.POST.get("gender")
        phone=req.POST.get("phone")
        address=req.POST.get("address")
        user=Customers(userid=userid,uname=uname,pwd=pwd,phone=phone,gender=gender,address=address)
        user.save()
        #send_mail('Registration Successfull','Your registration is now complete','smart.anandsingh@gmail.com',recipient_list=(userid,),fail_silently=False)
        return redirect('/login')
    return render(req,"register.html")

def loginpage(req):
    if(req.method=="POST"):
        userid=req.POST.get("userid")
        pwd=req.POST.get("pwd")
        user=Users.objects.filter(userid=userid,pwd=pwd)
        if(len(user)>0):
            print(user[0])
            req.session["userid"]=user[0].userid
            req.session["role"]='admin'
            req.session["uname"]=user[0].uname
            return redirect("/dashboard")                               
        else:
            cust=Customers.objects.filter(userid=userid,pwd=pwd)
            print(cust)
            if(len(cust)>0):
                req.session["userid"]=userid
                req.session["role"]='Customer'
                req.session["uname"]=cust[0].uname
                return redirect("/")
            else:
                messages.error(req, 'Invalid username or password') 
                return redirect("/login")           
    return render(req,"login.html")


def products(req,cid=0,size=''):
    print(cid)
    print(size)
    cats=Category.objects.all()
    if(cid>0):
        cat=Category.objects.get(pk=cid)
        cars=CarVariant.objects.filter(category=cat)
    elif(size!='' and size=='m'):
        cars=CarVariant.objects.filter(capacity__lte=5)
    elif(size!='' and size=='f'):
        cars=CarVariant.objects.filter(capacity__gt=5)
    else:
        cars=CarVariant.objects.all()
    if 'userid' in req.session:
        pass
        #msg="You are given a Discount of 30% from Delta Driving on any Car Price. Thank You."
    paginator=Paginator(cars,6)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(req,"products.html",locals())

def mybookings(req):
    user=Customers.objects.get(pk=req.session.get("userid"))    
    bks=Bookings.objects.filter(customer=user)
    return render(req,"mybookings.html",locals())

def bookingdetails(req,bid):
    bk=Bookings.objects.get(pk=bid)    
    print(bk)
    stages=JourneyStage.objects.filter(bookings=bk)
    check=JourneyStage.objects.filter(bookings=bk,status='Closed')
    paid=Payment.objects.filter(booking=bk,complete=True)
    print(paid)
    if(len(check)>0):
        closed=True
    if(len(paid)>0):
        phistory=Payment.objects.filter(booking=bk)
        complete=True
    else:
        bal=bk.billamount-bk.advance
        print(bal)
    return render(req,"bookdetails.html",locals())

def saveStage(req):
    bid=req.POST.get("bid")
    booking=Bookings.objects.get(pk=bid)
    stage=req.POST.get("stage")
    remarks=req.POST.get("remarks")    
    stage=JourneyStage(stage=stage,bookings=booking,remarks=remarks)
    if req.POST.get("status") is not None:
        stage.status='Closed'
    stage.save()
    return redirect(f"/bkdetails/{bid}")

def savePaymentAndFeedback(req):
    bid=req.POST.get("bid")
    bk=Bookings.objects.get(pk=bid)    
    nameoncard=req.POST.get("nameoncard")
    cardno=req.POST.get("cardno")
    balance=req.POST.get("balance")
    pymt=Payment(booking=bk,complete=True,nameoncard=nameoncard,cardno=cardno,amount=balance,remarks='Final Payment')
    pymt.save()
    fb=Feedback(customer=bk.customer,feedback=req.POST.get("feedback"),ratings=req.POST.get("rating"))
    fb.save()
    bk.startreading=bk.car.reading
    bk.returnreading=req.POST.get("reading")
    bk.save()
    car=bk.car
    car.reading=req.POST.get("reading")
    car.save()
    messages.success(req,"Payment made successfully")    
    return redirect(f"/bkdetails/{bid}")

def prod_details(req,cid):
    if(req.method=="POST"):
        fromdate=req.POST.get("fromdate")
        todate=req.POST.get("todate")
        message=req.POST.get("message")
        variant=CarVariant.objects.get(pk=req.POST.get("cid"))
        user=Customers.objects.get(pk=req.session.get("userid"))
        status='Pending'
        advance=req.POST.get("advance")
        pickuplocation=req.POST.get("pickuplocation")
        billamount=req.POST.get("billamount")
        bk=Bookings(fromdate=fromdate,todate=todate,message=message,variant=variant,customer=user,status=status,billamount=billamount, advance=advance,pickuplocation=pickuplocation)
        bk.save()
        bkinfo=Bookings.objects.latest('bid')
        cardno=req.POST.get("cardno")
        nameoncard=req.POST.get("nameoncard")
        remarks='Booking done'        
        pymt=Payment(booking=bkinfo,amount=advance,nameoncard=nameoncard,cardno=cardno,remarks=remarks)
        pymt.save()
        messages.success(req,"Car booked successfully")
        return redirect(f"/details/{cid}/")
    car=CarVariant.objects.get(pk=cid)  
    if 'userid' in req.session:
        user=Customers.objects.get(pk=req.session.get("userid"))
        if Bookings.objects.filter(customer=user).count()>2:
            #discount=car.price*0.10  
            pass
    return render(req,"product_details.html",locals())

def usercancelbooking(req,bid):
    bk=Bookings.objects.get(pk=bid)
    bk.delete()
    messages.success(req,"Booking Cancelled Successfully")
    return redirect("/mybookings")


def logout(req):
    req.session.flush()
    return redirect("/")