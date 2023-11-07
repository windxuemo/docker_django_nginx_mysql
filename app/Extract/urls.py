from django.urls import path
from .views import create_extract_firmware_task, update_extract_firmware_result, download_extract_firmware, get_all_tasks, get_completed_tasks, get_task_result, delete_extract_firmware_task

urlpatterns = [
    # 创建任务接口
    path('create-task/', create_extract_firmware_task, name='create-task'),

    # 下载固件接口
    path('download-firmware/<int:task_id>/', download_extract_firmware, name='download-firmware'),

    # 获取任务列表接口
    path('list-tasks/', get_all_tasks, name='list-tasks'),
    path('list-completed-tasks/', get_completed_tasks, name='list-completed-tasks'),

    # 删除任务接口
    path('delete-task/<int:task_id>/', delete_extract_firmware_task, name='delete-task'),

    # get result api
    path('update-result/', update_extract_firmware_result, name='update-result'),


    path('download-extracted-firmware/<int:task_id>/', get_task_result, name='download-extracted-firmware'),
]

