from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from urllib.parse import quote
from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId
from .models import AnalyzeBinaryTask
from .tasks import celery_send_task
import json



@login_required(login_url='/api/auth/login')
def create_task(request):
    if request.method == 'POST':
        # 处理用户上传的二进制文件并创建任务
        binary_file = request.FILES['binary_file']
        if binary_file:
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
            db = client['analyze_binary']

            # 获取 GridFS 实例
            fs = GridFS(db)

            # 存储固件文件到 GridFS
            binary_file_id = fs.put(binary_file.read(), filename=binary_file.name)


            task = AnalyzeBinaryTask.objects.create(
                binary_file_name=binary_file.name,
                binary_file_id=binary_file_id,
                created_at = timezone.now(),
                analysis_status='Pending'
            )

            celery_send_task(task.id)
            client.close()

            return JsonResponse({'message': '任务已创建', 'task_id': task.id})



@login_required(login_url='/api/auth/login')
def download_binary(request, task_id):
    try:
        analyze_task = AnalyzeBinaryTask.objects.get(id=task_id)
        if analyze_task.binary_file_id:
            mongo_config = settings.MONGO_CONFIG

            # 连接到 MongoDB
            client = MongoClient(
                host=mongo_config['host'],
                port=mongo_config['port'],
                username=mongo_config['username'],
                password=mongo_config['password'],
                maxPoolSize=mongo_config['max_pool_size']
            )

            db = client['analyze_binary']
 
            fs = GridFS(db)

            # 获取固件文件并返回给前端
            binary_file = fs.get(ObjectId(analyze_task.binary_file_id))
            binary_file_content = binary_file.read()
            binary_file_name = binary_file.filename

            # 关闭连接
            client.close()


            response = HttpResponse(binary_file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={quote(binary_file_name)}'
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

                analysis_task = AnalyzeBinaryTask.objects.get(id=task_id)
                analysis_task.analysis_result = result_data
                analysis_task.analysis_status = 'completed'
                analysis_task.save()
            elif status == 'failure':
                analysis_task = AnalyzeBinaryTask.objects.get(id=task_id)
                analysis_task.analysis_status = 'failed'
                analysis_task.save()


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Update successful'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/api/auth/login')
def list_all_task(request, task_id=None):
    page = request.GET.get('page')
    items_per_page = request.GET.get('items_per_page')

    tasks_data = AnalyzeBinaryTask.objects.all().order_by("id")

    paginator = Paginator(tasks_data, items_per_page)
    items = paginator.get_page(page)

    total_items = paginator.count
    task_list = [{'id': item.id, 'binary_name':item.binary_file_name, 'status': item.analysis_status, 'created_at': item.created_at,'result': item.analysis_result} for item in items]
    return JsonResponse({'tasks': task_list, 'total_items': total_items})




@login_required(login_url='/api/auth/login')
def list_task(request, task_id):

    task = AnalyzeBinaryTask.objects.get(id=task_id)
    task = {'id': task.id, 'binary_name':task.binary_file_name, 'result': task.analysis_result}
    return JsonResponse(task)






@login_required(login_url='/api/auth/login')
def delete_task(request, task_id):
    task = AnalyzeBinaryTask.objects.get(id=task_id)
    file_id = task.binary_file_id
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
       

    return JsonResponse({'message': 'Task deleted successfully.'})


