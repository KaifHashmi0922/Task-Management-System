from django.urls import path
from . import views

urlpatterns = [
    path('activity_list/', views.activity_list, name='activity_list'),
    path('create_activity/', views.create_activity, name='create_activity'),
    path('activity_detail/<int:id>/', views.activity_detail, name='activity_detail'),
    path('update_activity/<int:id>/', views.update_activity, name='update_activity'),
    path('update_activity/<int:id>/', views.delete_activity, name='delete_activity'),
]