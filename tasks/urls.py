
from django.urls import path
from tasks import views


urlpatterns = [
    path('activity/',views.activity,name="activity"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('label_list/',views.label_list,name='label_list'),
    path('project_detail/',views.project_detail,name='project_detail'),
    path('project_list/',views.project_list,name='project_list'),
    path('task_detail/',views.task_detail,name='task_detail'),
    path('task_list/',views.task_list,name='task_list'),
    path('project_register/',views.project_register,name='project_register'),
    path('task_create/',views.task_create,name='task_create'),
    path('project_delete/',views.project_delete,name='project_delete'),
    path('task_delete/',views.task_delete,name='task_delete'),
    
    
   
]
