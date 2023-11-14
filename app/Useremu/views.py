from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .models import UserEmulateTask
from Extract.models import ExtractFirmwareTask

from urllib.parse import quote
from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId
from .tasks import celery_send_task
from .tasks import celery_kill_task
import json


@login_required(login_url='/api/auth/login')
def list_all_task(request):
    page = request.GET.get('page')
    items_per_page = request.GET.get('items_per_page')

    tasks_data = UserEmulateTask.objects.all().order_by("id")
    paginator = Paginator(tasks_data, items_per_page)
    items = paginator.get_page(page)

    total_items = paginator.count
    task_list = [{'id': item.id, 'binary_name':item.binary_name, 'rootfs_name': item.rootfs_name, 'status': item.status, 'created_at': item.created_at, 'debug_ip': item.debug_ip, 'debug_port': item.debug_port} for item in items]
    return JsonResponse({'tasks': task_list, 'total_items': total_items})

@login_required(login_url='/api/auth/login')
def create_task(request):
    if request.method == 'POST':
        binary_file = request.FILES.get('binary_file')
        rootfs_file = request.FILES.get('rootfs_file')

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
        db = client['user_emulate']

        # 获取 GridFS 实例
        fs = GridFS(db)

        # 存储固件文件到 GridFS
        binary_file_id = fs.put(binary_file.read(), filename=binary_file.name)
        rootfs_file_id = fs.put(rootfs_file.read(), filename=rootfs_file.name)

        user_emulate_task = UserEmulateTask.objects.create()
        user_emulate_task.binary_file_id=str(binary_file_id)
        user_emulate_task.rootfs_file_id=str(rootfs_file_id)
        user_emulate_task.binary_name=binary_file.name
        user_emulate_task.rootfs_name=rootfs_file.name
        user_emulate_task.created_at = timezone.now()
        user_emulate_task.save()


        return JsonResponse({'message': '任务已创建', 'task_id': user_emulate_task.id})


@login_required(login_url='/api/auth/login')
def run_binary(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        args = request.POST.getlist('args', None)


        celery_send_task(task_id, args)

        return JsonResponse({'status': 'running', 'task_id': task_id})



@login_required(login_url='/api/auth/login')
def debug_binary(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        args = request.POST.getlist('args')

        user_emulate_task = UserEmulateTask.objects.get(id=task_id)
        user_emulate_task.status = 'emulating'
        user_emulate_task.save()

        celery_send_task(task_id, args)
        return JsonResponse({'status': 'debugging', 'task_id': task_id})
    return JsonResponse({'task_id': task_id, 'status': user_emulate_task.status})

@login_required(login_url='/api/auth/login')
def update_result(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)

            task_id = request_data.get('task_id')
            status = request_data.get('status')
            if status == 'success':
                debug_ip = request_data.get('ip')
                debug_port = request_data.get('port')
                pid = request_data.get('pid')

                emulate_task = UserEmulateTask.objects.get(id=task_id)
                emulate_task.status = 'listening'
                emulate_task.debug_ip = debug_ip
                emulate_task.debug_port = debug_port
                emulate_task.pid = pid
                emulate_task.save()
            elif status == 'failed':
                emulate_task = UserEmulateTask.objects.get(id=task_id)
                emulate_task.status = 'failed'
                emulate_task.save()
            elif status == 'terminated':
                emulate_task = UserEmulateTask.objects.get(id=task_id)
                emulate_task.debug_ip = None
                emulate_task.debug_port = None
                emulate_task.pid = None
                emulate_task.status = 'closed'
                emulate_task.save()


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Update successful'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/api/auth/login')
def terminate_task(request):
    if request.method == 'POST':
        try:
            task_id = request.POST.get('task_id')
            task = UserEmulateTask.objects.get(id=task_id)
            pid = task.pid
            celery_kill_task(task_id, pid)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    return JsonResponse({'message': '任务已terminated', 'task_id': task_id})




@login_required(login_url='/api/auth/login')
def download_bin(request, task_id):
    try:
        task = UserEmulateTask.objects.get(id=task_id)
        if task.binary_file_id:
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )

            db = client['user_emulate']
 
            fs = GridFS(db)

            # 获取固件文件并返回给前端
            binary_file = fs.get(ObjectId(task.binary_file_id))
            binary_file_content = binary_file.read()
            binary_file_name = binary_file.filename

            # 关闭连接
            client.close()


            response = HttpResponse(binary_file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={quote(binary_file_name)}'
            return response

        else:
            return JsonResponse({'error': '文件不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@login_required(login_url='/api/auth/login')
def download_rootfs(request, task_id):
    try:
        task = UserEmulateTask.objects.get(id=task_id)
        if task.rootfs_file_id:
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )

            db = client['user_emulate']
 
            fs = GridFS(db)

            # 获取固件文件并返回给前端
            rootfs_file = fs.get(ObjectId(task.rootfs_file_id))
            rootfs_file_content = rootfs_file.read()
            rootfs_file_name = rootfs_file.filename

            # 关闭连接
            client.close()


            response = HttpResponse(rootfs_file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={rootfs_file_name}'
            return response

        else:
            return JsonResponse({'error': '固件文件不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@login_required(login_url='/api/auth/login')
@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = UserEmulateTask.objects.get(id=task_id)
            binary_file_id = task.binary_file_id
            rootfs_file_id = task.rootfs_file_id

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

            db = client['user_emulate']
 
            fs = GridFS(db)
            fs.delete(ObjectId(binary_file_id))
            fs.delete(ObjectId(rootfs_file_id))

            client.close()

            task.delete()
            return JsonResponse({'message': '任务删除成功'})
        except UserEmulateTask.DoesNotExist:
            return JsonResponse({'error': '任务不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

