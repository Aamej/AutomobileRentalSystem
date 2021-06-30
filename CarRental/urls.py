"""CarRental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static,settings
from carapp import views
from adminapp import views as v1

urlpatterns = [
    path('',views.homepage),
    path('login/',views.loginpage),
    path('contact/',views.contactus),
    path('about/',views.aboutus),
    path('logout/',views.logout),
    path('register/',views.registerpage),
    path('dashboard/',v1.dashboard),
    path('cats/',v1.categories),
    path('cats/<int:cid>',v1.categories),
    path('delcat/<int:cid>',v1.deletecategpry),
    path('variants/',v1.carvariants),
    path('cars/',v1.cars),
    path('cars/<str:carno>',v1.cars),
    path('drivers/',v1.drivers),
    path('feedbacks/',v1.feedbacks),
    path('reports/',v1.reports),
    path('adddriver/',v1.adddriver),
    path('products/',views.products),
    path('products/b/<int:cid>',views.products),
    path('products/s/<str:size>',views.products),
    path('details/<int:cid>/',views.prod_details),
    path('bookings/',v1.bookings),
    path('bdetails/<int:bid>',v1.booking_details),
    path('mybookings/',views.mybookings),
    path('bkdetails/<int:bid>',views.bookingdetails),
    path('savestage/',views.saveStage),
    path('savepymt/',views.savePaymentAndFeedback),
    path('cancel/<int:bid>',views.usercancelbooking),
    path('admincancel/<int:bid>',v1.cancelbooking),
    path('confirm/<int:bid>',v1.confirmbooking),
    path('users/',v1.userspage),
    path('addcar/',v1.addCar),
    path('editcar/<int:cid>/',v1.editcar),
    path('changepwd/',v1.changepwd),
    path('admin/', admin.site.urls),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
