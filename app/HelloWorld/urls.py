from django.urls import path
from .views import CreateTaskView, DownloadFirmwareView, ListTasksView, DeleteTaskView, GetResultView

urlpatterns = [
    # 创建任务接口
    path('create-task/', CreateTaskView.as_view(), name='create-task'),

    # 下载固件接口
    path('download-firmware/<int:task_id>/', DownloadFirmwareView.as_view(), name='download-firmware'),

    # 获取任务列表接口
    path('list-tasks/', ListTasksView.as_view(), name='list-tasks'),

    # 删除任务接口
    path('delete-task/<int:task_id>/', DeleteTaskView.as_view(), name='delete-task'),

    # get result api
    path('update-result/', GetResultView.as_view(), name='update-result'),
]

