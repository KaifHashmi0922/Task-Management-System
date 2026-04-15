
from django.urls import path
from users import views


urlpatterns = [
    path('profile_edit/',views.profile_edit,name="profile_edit"),
    path('profile/',views.profile,name='profile'),
    path('users_list/',views.users_list,name='users_list'),
  
   
    
      
]
