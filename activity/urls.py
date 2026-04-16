from django.urls import path
from activity import views

urlpatterns = [
    path('activitys/',views.activitys,name='activitys'),
]
