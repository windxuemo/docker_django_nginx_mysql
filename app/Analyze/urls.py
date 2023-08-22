
from django.urls import path
from .views import create_analyze_firmware_task, select_and_create_task, download_firmware, update_result, list_task, list_all_task, delete_task

urlpatterns = [
    path('create-task/', create_analyze_firmware_task, name='create-task'),
    path('select-create-task/', select_and_create_task, name='select-create-task'),
    path('update-result/', update_result, name='update-result'),
    path('download-firmware/<int:task_id>/', download_firmware, name='download-firmware'),
    path('list-all-task/', list_all_task, name='list-all-tasks'),
    path('list-task/<int:task_id>', list_task, name='list-tasks'),
    path('delete-task/<int:task_id>/', delete_task, name='delete-task'),
]

