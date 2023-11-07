
from django.urls import path
from .views import create_task, download_binary, update_result, list_task, list_all_task, delete_task

urlpatterns = [
    path('create-task/', create_task, name='create-task'),
    path('update-result/', update_result, name='update-result'),
    path('download-binary/<int:task_id>/', download_binary, name='download-binary'),
    path('list-tasks/', list_all_task, name='list-tasks'),
    path('list-task/<int:task_id>', list_task, name='list-tasks'),
    path('delete-task/<int:task_id>/', delete_task, name='delete-task'),
]

