
from django.urls import path
from accounts import views


urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/',views.register,name="register"),
    path('',views.login,name='login'),
     path('logout/',views.logout,name='logout'),
    
    path('forget_password/',views.forget_password,name='forget_password'),\
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('reset_password',views.reset_password,name='reset_password'),
    
   
]
