
from django.urls import path
from accounts import views


urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('register/',views.register,name="register"),
    path('login/',views.login,name='login'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('reset_password',views.reset_password,name='reset_password'),
    
   
]
