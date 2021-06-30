from django.db.models.query import ValuesIterable
from django.shortcuts import render,redirect
from carapp.models import Customers,Users,CarVariant,Category,JourneyStage,Feedback,Drivers,Payment,Bookings,Car
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator

# Create your views here.
def dashboard(req):
    totalbrands=Category.objects.count()
    totalcarvars=CarVariant.objects.count()
    totalcars=Car.objects.count()
    totalbookings=Bookings.objects.filter(status='Pending').count()
    totalusers=Users.objects.count()
    totaldrivers=Drivers.objects.count()
    return render(req,"dashboard.html",locals())

def categories(req,cid=0):
    if(req.method=="POST"):  
        cat=Category()    
        cat.id=req.POST.get('id')  
        cat.catname=req.POST.get('catname')  
        cat.description=req.POST.get("descr")
        if req.FILES.get("pic") is not None:
            cat.photo=req.FILES.get("pic") 
        else:
            cat.photo=Category.objects.get(pk=req.POST.get('id')).photo       
        cat.save()
        messages.success(req,"Category saved successfully")
        return redirect("/cats")
    if(cid>0):
        cat=Category.objects.get(pk=cid)
    cats=Category.objects.all()
    #cats=('Economy','Compact','Mid Size','Full Size','Premium','Luxury','Minivan','Standard SUV','Full Size SUV')
    #cats=('Hatchback','Sedan','MPV or MUV','SUV Sports Utility Vehicle','Crossover','Coupe','Convertible')
    paginator=Paginator(cats,5)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    totalpages=range(1,page_obj.paginator.num_pages+1)
    return render(req,"categories.html",locals())

def deletecategpry(req,cid):
    b=Category.objects.get(pk=cid)
    b.delete()
    messages.success(req,"Category deleted successfully")
    return redirect("/cats")

def carvariants(req):
    vcars=CarVariant.objects.all()
    paginator=Paginator(vcars,10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    totalpages=range(1,page_obj.paginator.num_pages+1)
    return render(req,"carvariants.html",locals())

def cars(req,carno=None):
    if req.method=="POST":
        carno=req.POST.get("carno")
        variant=CarVariant.objects.get(pk=req.POST.get("vid"))
        modelyear=req.POST.get("modelyear")
        reading=req.POST.get("reading")
        car=Car(carno=carno,carv=variant,modelyear=modelyear,reading=reading)
        car.save()
        messages.success(req,"Car saved successfully")
        return redirect("/cars")
    cars=Car.objects.filter(deleted=False)
    if carno is not None:
        car=Car.objects.get(pk=carno)
    variants=CarVariant.objects.all()    
    paginator=Paginator(cars,10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(req,"cars.html",locals())

def drivers(req):
    drivers=Drivers.objects.all()
    paginator=Paginator(drivers,10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(req,"drivers.html",locals())

def feedbacks(req):
    fb=Feedback.objects.all()
    return render(req,"feedbacks.html",locals())

def adddriver(req):
    if(req.method=="POST"):
        dname=req.POST.get("dname")
        address=req.POST.get("address")
        gender=req.POST.get("gender")
        mstatus=req.POST.get("mstatus")
        phone=req.POST.get("phone")
        adhar=req.POST.get("adhar")
        exp=req.POST.get("exp")
        licno=req.POST.get("licno")
        dob=req.POST.get("dob")
        
        driver=Drivers(dname=dname,gender=gender,mstatus=mstatus,dob=dob,exp=exp,licno=licno,adhar=adhar,phone=phone,address=address)
        if req.FILES.get("photo") is not None:
            driver.photo=req.FILES.get("photo")
        driver.save()
        messages.success(req,"Driver added successfully")
        return redirect("/drivers")
    return render(req,"newdriver.html",locals())

def reports(req):
    pmt=Payment.objects.all()
    paginator=Paginator(pmt,10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(req,"reports.html",locals())

def booking_details(req,bid):
    bk=Bookings.objects.get(pk=bid)
    if req.method=="POST":
        bk.status='Confirmed'
        bk.car=Car.objects.get(pk=req.POST.get("cid"))
        bk.driver=Drivers.objects.get(pk=req.POST.get("driver"))
        bk.save()
        messages.success(req,"Booking confirmed")
        return redirect("/bookings")
    
    cars=Car.objects.filter(carv=bk.variant)
    drivers=Drivers.objects.all()
    phistory=Payment.objects.filter(booking=bk)
    return render(req,"book-details.html",locals())

def confirmbooking(req,bid):
    bk=Bookings.objects.get(pk=bid)
    bk.status="Confirmed"
    bk.save()
    messages.success(req,"Booking confirmed")
    return redirect("/bookings")

def cancelbooking(req,bid):
    bk=Bookings.objects.get(pk=bid)
    bk.delete()
    messages.success(req,"Booking cancelled")
    return redirect("/bookings")

def addCar(req):
    if(req.method=="POST"):
        car=CarVariant()
        car.title=req.POST.get("title")
        car.fueltype=req.POST.get("fueltype")
        car.price=req.POST.get("price")
        car.capacity=req.POST.get("capacity")
        car.category=Category.objects.get(pk=req.POST.get("cid"))
        car.ac=req.POST.get("ac")=="on"
        car.powerdoorlock=req.POST.get("powerdoorlock")=="on"
        car.powersteering=req.POST.get("powersteering")=="on"
        car.powerwindows=req.POST.get("powerwindows")=="on"
        car.cdplayer=req.POST.get("cdplayer")=="on"
        car.centrallock=req.POST.get("centrallock")=="on"
        car.airbag=req.POST.get("airbag")=="on"
        car.gps=req.POST.get("gps")=="on"
        car.photo=req.FILES.get("photo")
        car.save()
        messages.success(req,"Car Variant added successfully")
        return redirect("/variants")
    cats=Category.objects.all()
    fueltypes=('Petrol','Diesel','CNG')
    return render(req,"newcar.html",locals())

def editcar(req,cid):
    if(req.method=="POST"):
        car=CarVariant.objects.get(pk=cid)
        car.title=req.POST.get("title")
        car.fueltype=req.POST.get("fueltype")
        car.price=req.POST.get("price")
        car.capacity=req.POST.get("capacity")
        car.category=Category.objects.get(pk=cid)
        car.ac=req.POST.get("ac")=="on"
        car.powerdoorlock=req.POST.get("powerdoorlock")=="on"
        car.powersteering=req.POST.get("powersteering")=="on"
        car.powerwindows=req.POST.get("powerwindows")=="on"
        car.cdplayer=req.POST.get("cdplayer")=="on"
        car.centrallock=req.POST.get("centrallock")=="on"
        car.airbag=req.POST.get("airbag")=="on"
        car.gps=req.POST.get("gps")=="on"
        print(car.photo)
        print(req.FILES.get("photo"))
        if(req.FILES.get("photo") is not None):
            car.photo=req.FILES.get("photo")
        car.save()
        messages.success(req,"Car Variant updated successfully")
        return redirect("/variants")
    car=CarVariant.objects.get(pk=cid)
    cats=Category.objects.all()
    fueltypes=('Petrol','Diesel','CNG')
    return render(req,"editcar.html",locals())

def bookings(req):
    bks=Bookings.objects.all()
    paginator=Paginator(bks,10)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    totalpages=range(1,page_obj.paginator.num_pages+1)
    return render(req,"bookings.html",locals())

def userspage(req):
    users=Customers.objects.all()
    return render(req,"users.html",locals())

def changepwd(req):
    if(req.method=="POST"):
        userid=req.session["userid"]
        user=Users.objects.get(pk=userid)
        if(user.pwd==req.POST.get("opwd")):
            user.pwd=req.POST.get("pwd")
            user.save()
            messages.success(req,"Password updated successfully")
        else:
            messages.error(req,"Incorrect current password")
    return redirect("/dashboard")