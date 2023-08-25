from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse

from .models import EmulateFirmwareTask
from HelloWorld.models import ExtractFirmwareTask

from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId
from .tasks import celery_send_task
from .tasks import celery_kill_task
import json

@csrf_exempt
def create_emulate_firmware_task(request):
    if request.method == 'POST':
        try:
            firmware_file = request.FILES.get('firmware_file')
            if firmware_file:

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
                db = client['emulate_firmware']

                # 获取 GridFS 实例
                fs = GridFS(db)

                # 存储固件文件到 GridFS
                file_id = fs.put(firmware_file.read(), filename=firmware_file.name)


                emulate_task = EmulateFirmwareTask.objects.create()
                emulate_task.file_id=str(file_id)
                emulate_task.firmware_name=firmware_file.name
                emulate_task.status = 'emulating'
                emulate_task.save()

                celery_send_task(emulate_task.id)
                client.close()

                return JsonResponse({'message': '任务已创建', 'task_id': emulate_task.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def select_and_create_task(request):
    import pdb
    pdb.set_trace()
    if request.method == 'POST':
        try:
            extract_task_id = request.POST.get('task_id')
            if extract_task_id:

                extract_task = ExtractFirmwareTask.objects.get(id=extract_task_id)

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
                extract_db = client['extract_firmware']
                emulate_db = client['emulate_firmware']

                # 获取 GridFS 实例
                extract_fs = GridFS(extract_db)

                firmware_file = extract_fs.get(ObjectId(extract_task.file_id))
                firmware_file_content = firmware_file.read()
                firmware_file_name = firmware_file.filename

                emulate_fs = GridFS(emulate_db)

                # 存储固件文件到 GridFS
                file_id = emulate_fs.put(firmware_file_content, filename=firmware_file_name)

                emulate_task = EmulateFirmwareTask.objects.create()
                emulate_task.file_id=str(file_id)
                emulate_task.firmware_name=firmware_file_name
                emulate_task.status = 'emulating'
                emulate_task.save()

                celery_send_task(emulate_task.id)
                client.close()

                return JsonResponse({'message': '任务已创建', 'task_id': emulate_task.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def terminate_firmware_task(request):
    import pdb
    pdb.set_trace()
    if request.method == 'POST':
        try:
            task_id = request.POST.get('task_id')
            task = EmulateFirmwareTask.objects.get(id=task_id)
            pid = task.pid
            celery_kill_task(task_id, pid)


            task.status = 'terminating'
            task.pid = None
            task.save()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    return JsonResponse({'message': '任务已terminated', 'task_id': task_id})



def download_firmware(request, task_id):
    try:
        emulate_task = EmulateFirmwareTask.objects.get(id=task_id)
        if emulate_task.file_id:
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )

            db = client['emulate_firmware']
 
            fs = GridFS(db)

            # 获取固件文件并返回给前端
            firmware_file = fs.get(ObjectId(emulate_task.file_id))
            firmware_file_content = firmware_file.read()
            firmware_file_name = firmware_file.filename

            # 关闭连接
            client.close()


            response = HttpResponse(firmware_file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={firmware_file_name}'
            return response

        else:
            return JsonResponse({'error': '固件文件不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def update_result(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)

            task_id = request_data.get('task_id')
            status = request_data.get('status')
            if status == 'success':
                web_ip = request_data.get('web_ip')
                nginx_ip = request_data.get('nginx_ip')
                pid = request_data.get('pid')

                emulate_task = EmulateFirmwareTask.objects.get(id=task_id)
                emulate_task.status = 'completed'
                emulate_task.web_ip = web_ip
                emulate_task.nginx_ip = nginx_ip
                emulate_task.pid = pid
                emulate_task.save()
            elif status == 'failure':
                emulate_task = EmulateFirmwareTask.objects.get(id=task_id)
                emulate_task.status = 'failed'
                emulate_task.save()


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Update successful'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def list_all_task(request, task_id=None):
    tasks = EmulateFirmwareTask.objects.all()
    task_list = [{'id': task.id, 'firmware_name':task.firmware_name, 'status': task.status, 'nginx_ip': task.nginx_ip} for task in tasks]
    return JsonResponse({'tasks': task_list})




def list_task(request, task_id):

    task = EmulateFirmwareTask.objects.get(id=task_id)
    task = {'id': task.id, 'firmware_name':task.firmware_name, 'result': task.firmware_result}
    return JsonResponse(task)


@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = AnalyzeFirmwareTask.objects.get(id=task_id)
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

            db = client['emulate_firmware']
 
            fs = GridFS(db)
            fs.delete(ObjectId(file_id))

            client.close()

            task.delete()
            return JsonResponse({'message': '任务删除成功'})
        except AnalyzeFirmwareTask.DoesNotExist:
            return JsonResponse({'error': '任务不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

