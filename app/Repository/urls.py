from django.urls import path
from .views import firmware_upload, firmware_list, download_firmware, delete_firmware, update_vendor

urlpatterns = [
    # 创建任务接口
    path('upload-firmware/', firmware_upload, name='firmware-upload'),

    # 下载固件接口
    path('download-firmware/<int:task_id>/', download_firmware, name='download-firmware'),

    # 获取任务列表接口
    path('list-firmwares/', firmware_list, name='firmware-list'),
    # 
    path('update-vendor/', update_vendor, name='update-vendor'),

    # 删除任务接口
    path('delete-firmware/<int:task_id>/', delete_firmware, name='delete-firmware')

]

