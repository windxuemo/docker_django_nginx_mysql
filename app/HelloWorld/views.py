# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.http import HttpResponse

from django.views import View
from django.conf import settings
from .models import ExtractFirmwareTask
from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId

from .tasks import celery_send_task

class CreateTaskView(View):
    def post(self, request):
        firmware_file = request.FILES.get('firmware')

        if firmware_file:
            # 解析固件名称
            firmware_name = firmware_file.name

            # 从 settings.py 中读取 MongoDB 连接参数
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )
            db = client['extract_firmware']

            # 获取 GridFS 实例
            fs = GridFS(db)

            # 存储固件文件到 GridFS
            file_id = fs.put(firmware_file.read(), filename=firmware_file.name)


            # 创建任务记录
            task = ExtractFirmwareTask.objects.create(file_id=str(file_id), firmware_name=firmware_name, status='unpacking')
            celery_send_task(task.id)

            # 关闭连接
            client.close()

            return JsonResponse({'message': '任务已创建', 'task_id': task.id})
        else:
            return JsonResponse({'message': '未提供固件文件'}, status=400)

class GetResultView(View):
    def post(self, request):
        try:
            task_id = request.POST.get('task_id')
            extracted_file = request.FILES.get('zip_file')

            if not task_id or not extracted_file:
                return JsonResponse({'error': 'Missing parameters'}, status=400)
            # 从 settings.py 中读取 MongoDB 连接参数
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )
            db = client['extract_firmware']

            # 获取 GridFS 实例
            fs = GridFS(db)

            # 存储固件文件到 GridFS
            file_id = fs.put(extracted_file.read(), filename=extracted_file.name)


            try:
                extract_firmware_task = ExtractFirmwareTask.objects.get(id=task_id)
                extract_firmware_task.extracted_file_id = str(file_id)
                extract_firmware_task.status = 'completed'
                extract_firmware_task.save()
            except ExtractFirmwareTask.DoesNotExist:
                return JsonResponse({'error': 'Task not found'}, status=404)

            return JsonResponse({'message': 'Update successful'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)





class DownloadFirmwareView(View):
    def get(self, request, task_id):
        try:
            task = ExtractFirmwareTask.objects.get(id=task_id)
            # 连接到 MongoDB
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )

            db = client['extract_firmware']
 
            fs = GridFS(db)

            # 获取固件文件并返回给前端
            firmware_file = fs.get(ObjectId(task.file_id))
            firmware_file_content = firmware_file.read()
            firmware_file_name = firmware_file.filename

            # 关闭连接
            client.close()

            response = HttpResponse(firmware_file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={firmware_file_name}'

            return response
        except ExtractFirmwareTask.DoesNotExist:
            return JsonResponse({'message': '任务不存在'}, status=404)

class ListTasksView(View):
    def get(self, request):
        tasks = ExtractFirmwareTask.objects.all()
        task_list = [{'id': task.id, 'status': task.status, 'firmware_name': task.firmware_name} for task in tasks]
        return JsonResponse({'tasks': task_list})

class DeleteTaskView(View):
    def post(self, request, task_id):
        try:
            task = ExtractFirmwareTask.objects.get(id=task_id)
            file_id = task.file_id
            # 连接到 MongoDB
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )

            db = client['extract_firmware']
 
            fs = GridFS(db)
            fs.delete(ObjectId(file_id))

            client.close()

            task.delete()
            return JsonResponse({'message': '任务已删除'})
        except ExtractFirmwareTask.DoesNotExist:
            return JsonResponse({'message': '任务不存在'}, status=404)

