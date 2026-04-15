
from django.urls import path
from tasks import views



urlpatterns = [
    
    
    path('activity/',views.activity,name="activity"),
   
    path('label_list/',views.label_list,name='label_list'),
    path('project_detail/<int:id>',views.project_detail,name='project_detail'),
    path('project_list/',views.project_list,name='project_list'),
    path('task_detail/<int:id>',views.task_detail,name='task_detail'),
    path('task_list/',views.task_list,name='task_list'),
    path('project_create/',views.project_create,name='project_create'),
    path('task_create/',views.task_create,name='task_create'),
    path('project_delete/<int:id>',views.project_delete,name='project_delete'),
    path('project_update/<int:id>',views.project_update,name='project_update'),
    path('task_delete/<int:id>',views.task_delete,name='task_delete'),
    path('task_update/<int:id>',views.task_update,name='task_update'),
    
    
    
]
