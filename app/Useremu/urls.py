
from django.urls import path
from .views import create_task, debug_binary, download_rootfs, download_bin, list_all_task, delete_task, update_result, terminate_task

urlpatterns = [
    path('create-task/', create_task, name='create-task'),
    # path('select-create-task/', select_and_create_task, name='select-create-task'),
    path('debug/', debug_binary, name='debug'),
    path('update-result/', update_result, name='update-result'),
    path('terminate-task/', terminate_task, name='terminate-task'),
    # path('update-result/', update_result, name='update-result'),
    path('download-rootfs/<int:task_id>/', download_rootfs, name='download-rootfs'),
    path('download-bin/<int:task_id>/', download_bin, name='download-bin'),
    path('list-tasks/', list_all_task, name='list-all-task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete-task'),
]

