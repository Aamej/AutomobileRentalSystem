from django.db import models
from django.db.models.base import Model

# Create your models here.
class Users(models.Model):  #for admins
    userid=models.CharField(max_length=40,primary_key=True)
    uname=models.CharField(max_length=50)
    pwd=models.CharField(max_length=20)
    
    class Meta:
        db_table="users"


class Customers(models.Model):
    userid=models.CharField(max_length=40,primary_key=True)
    uname=models.CharField(max_length=50)
    pwd=models.CharField(max_length=20)
    phone=models.CharField(max_length=10,null=True)
    gender=models.CharField(max_length=12,null=True)
    address=models.CharField(max_length=40,null=True)
    createdon=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table="customers"
        ordering=['-createdon']


class Category(models.Model):
    id=models.AutoField(primary_key=True)
    catname=models.CharField(max_length=30,null=True)
    description=models.CharField(max_length=2000,null=True)
    photo=models.ImageField(upload_to='cats',default='noimage.png')
    
    class Meta:
        db_table="categories"
        ordering=['-id']


class CarVariant(models.Model):
    cid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=30)
    category=models.ForeignKey(to=Category,on_delete=models.CASCADE)
    price=models.DecimalField(decimal_places=2,max_digits=12,default=0.00)
    fueltype=models.CharField(max_length=20)    
    capacity=models.IntegerField()
    #features
    ac=models.BooleanField(default=False)
    powerdoorlock=models.BooleanField(default=False)
    powersteering=models.BooleanField(default=False)
    airbag=models.BooleanField(default=False)
    powerwindows=models.BooleanField(default=False)
    cdplayer=models.BooleanField(default=False)
    centrallock=models.BooleanField(default=False)
    gps=models.BooleanField(default=False)

    photo=models.ImageField(upload_to='pics',default='noimage.png')
    createdon=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="cars"
        ordering=['-cid']

class Car(models.Model):
    carno=models.CharField(max_length=12,primary_key=True)
    modelyear=models.IntegerField()
    carv=models.ForeignKey(to=CarVariant,on_delete=models.CASCADE)
    reading=models.IntegerField()
    status=models.CharField(max_length=20,default='Available') # Available, On Booking
    active=models.BooleanField(default=True)
    deleted=models.BooleanField(default=False)
    createdon=models.DateTimeField(auto_now=True)

    class Meta:        
        db_table="registeredcars"
        ordering=['-createdon']

class Drivers(models.Model):
    id=models.AutoField(primary_key=True)
    dname=models.CharField(max_length=30)
    address=models.CharField(max_length=40)
    gender=models.CharField(max_length=12)
    mstatus=models.CharField(max_length=12,null=True)
    licno=models.CharField(max_length=20)
    phone=models.CharField(max_length=10)
    adhar=models.CharField(max_length=12)
    dob=models.DateField()
    exp=models.IntegerField(null=True)
    photo=models.ImageField(upload_to='drivers',default='noimage.png')
    status=models.CharField(max_length=20,default='Available') #On Leave, On Duty,Resigned
    active=models.BooleanField(default=True)
    deleted=models.BooleanField(default=False)
    createdon=models.DateTimeField(auto_now=True)

    class Meta:
        db_table="drivers"
        ordering=["-createdon"]


class Bookings(models.Model):
    bid=models.AutoField(primary_key=True)
    customer=models.ForeignKey(to=Customers,on_delete=models.CASCADE,null=True)
    advance=models.DecimalField(decimal_places=2,max_digits=15,default=0) #advance money paid
    fromdate=models.DateField()
    todate=models.DateField()
    message=models.CharField(max_length=400)
    bookingdate=models.DateField(auto_now=True)
    status=models.CharField(max_length=20,default='Pending') #Pending Confirmed Cancelled
    startreading=models.IntegerField(null=True)
    returnreading=models.IntegerField(null=True)
    pickuplocation=models.CharField(max_length=100,null=True)
    billamount=models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    variant=models.ForeignKey(to=CarVariant,on_delete=models.CASCADE,null=True)
    car=models.ForeignKey(to=Car,on_delete=models.CASCADE,null=True)  
    driver=models.ForeignKey(to=Drivers,on_delete=models.CASCADE,null=True)  

    class Meta:
        db_table="bookings"
        ordering=['-bid']

class JourneyStage(models.Model):
    id=models.AutoField(primary_key=True)
    bookings=models.ForeignKey(to=Bookings,on_delete=models.CASCADE)
    stage=models.CharField(max_length=30) # Not Started, Car Arrive, Journey Begin, On the way, Journey Completed 
    stagetime=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20,default='Open') # Open Closed
    remarks=models.CharField(max_length=50,null=True)

    class Meta:
        db_table='journeystages'
        ordering=['-id'] 

class Feedback(models.Model):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(to=Customers,on_delete=models.CASCADE)
    ratings=models.IntegerField(null=True)
    feedback=models.CharField(max_length=1000)
    createdon=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='feedbacks'
        ordering=['-id']  


class Payment(models.Model):
    pid=models.AutoField(primary_key=True)
    pymtdate=models.DateField(auto_now=True)
    booking=models.ForeignKey(to=Bookings,on_delete=models.CASCADE)
    #paymentmethod=models.CharField(max_length=20,null=True) # UPI, Internet Banking, Debit Card, Credit Card
    cardno=models.CharField(max_length=20,null=True)
    nameoncard=models.CharField(max_length=40,null=True)
    remarks=models.CharField(max_length=50,null=True)
    complete=models.BooleanField(default=False)
    amount=models.DecimalField(max_digits=14,decimal_places=2,default=0.00)

    class Meta:
        db_table="payments"
        ordering=['-pid']


