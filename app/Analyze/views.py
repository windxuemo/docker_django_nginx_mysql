from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import AnalyzeFirmwareTask
from Extract.models import ExtractFirmwareTask

from urllib.parse import quote
from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId
from .tasks import celery_send_task
import json

@login_required(login_url='/api/auth/login')
@csrf_exempt
def create_analyze_firmware_task(request):
    if request.method == 'POST':
        try:
            zip_file = request.FILES.get('zip_file')
            if zip_file:


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
                db = client['analyze_firmware']

                # 获取 GridFS 实例
                fs = GridFS(db)

                # 存储固件文件到 GridFS
                file_id = fs.put(zip_file.read(), filename=zip_file.name)


                analyze_task = AnalyzeFirmwareTask.objects.create()
                analyze_task.file_id=str(file_id)
                analyze_task.firmware_name=zip_file.name
                analyze_task.status = 'analyzing'
                analyze_task.created_at = timezone.now()
                analyze_task.save()

                celery_send_task(analyze_task.id)
                client.close()

                return JsonResponse({'message': '任务已创建', 'task_id': analyze_task.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/api/auth/login')
@csrf_exempt
def select_and_create_task(request):
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
                analyze_db = client['analyze_firmware']

                # 获取 GridFS 实例
                extract_fs = GridFS(extract_db)

                zip_file = extract_fs.get(ObjectId(extract_task.extracted_file_id))
                zip_file_content = zip_file.read()
                zip_file_name = zip_file.filename

                analyze_fs = GridFS(analyze_db)

                # 存储固件文件到 GridFS
                file_id = analyze_fs.put(zip_file_content, filename=zip_file_name)

                analyze_task = AnalyzeFirmwareTask.objects.create()
                analyze_task.file_id=str(file_id)
                analyze_task.firmware_name=zip_file.name
                analyze_task.status = 'analyzing'
                analyze_task.created_at = timezone.now()
                analyze_task.save()

                celery_send_task(analyze_task.id)
                client.close()

                return JsonResponse({'message': '任务已创建', 'task_id': analyze_task.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@login_required(login_url='/api/auth/login')
def download_firmware(request, task_id):
    try:
        analyze_task = AnalyzeFirmwareTask.objects.get(id=task_id)
        if analyze_task.file_id:
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )

            db = client['analyze_firmware']
 
            fs = GridFS(db)

            # 获取固件文件并返回给前端
            zip_file = fs.get(ObjectId(analyze_task.file_id))
            zip_file_content = zip_file.read()
            zip_file_name = zip_file.filename

            # 关闭连接
            client.close()


            response = HttpResponse(zip_file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={quote(zip_file_name)}'
            return response

        else:
            return JsonResponse({'error': '固件文件不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/api/auth/login')
def update_result(request):
    if request.method == 'POST':
        try:

            request_data = json.loads(request.body)

            task_id = request_data.get('task_id')
            status = request_data.get('status')
            if status == 'success':
                result_data = request_data.get('result_data')
                arch_info = request_data.get('arch')

                analysis_task = AnalyzeFirmwareTask.objects.get(id=task_id)
                analysis_task.firmware_result = result_data
                analysis_task.arch = arch_info
                analysis_task.status = 'completed'
                analysis_task.save()
            elif status == 'failure':
                analysis_task = AnalyzeFirmwareTask.objects.get(id=task_id)
                analysis_task.status = 'failed'
                analysis_task.save()


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Update successful'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/api/auth/login')
def list_all_task(request, task_id=None):
    page = request.GET.get('page')
    items_per_page = request.GET.get('items_per_page')


    tasks_data = AnalyzeFirmwareTask.objects.all().order_by("id")

    paginator = Paginator(tasks_data, items_per_page)
    items = paginator.get_page(page)

    total_items = paginator.count

    task_list = [{'id': item.id, 'firmware_name':item.firmware_name, 'created_at': item.created_at, 'status': item.status} for item in items]
    return JsonResponse({'tasks': task_list, 'total_items': total_items})




@login_required(login_url='/api/auth/login')
def list_task(request, task_id):

    task = AnalyzeFirmwareTask.objects.get(id=task_id)
    task = {'id': task.id, 'firmware_name':task.firmware_name, 'result': task.firmware_result}
    return JsonResponse(task)


@login_required(login_url='/api/auth/login')
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

            db = client['analyze_firmware']
 
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

