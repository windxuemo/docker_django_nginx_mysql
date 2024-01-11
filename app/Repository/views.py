# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.views import View
from django.conf import settings
from .models import FirmwareRepository
from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.utils import timezone
from urllib.parse import quote



@login_required(login_url='/api/auth/login')
def firmware_upload(request):

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
    db = client['firmware_repository']

    # 获取 GridFS 实例
    fs = GridFS(db)

    firmware_files = request.FILES.getlist('files')
    print("---------1111-----")
    vendor = request.POST.get('vendor')
    print("---------222-----")
    print(vendor)

    for firmware_file in firmware_files:

        firmware_name = firmware_file.name
        print(firmware_name)
        print(vendor)
        # 存储固件文件到 GridFS
        file_id = fs.put(firmware_file.read(), filename=firmware_file.name)

        # 创建任务记录
        firmware = FirmwareRepository.objects.create(file_id=str(file_id), name=firmware_name, vendor=vendor, created_at = timezone.now())

    # 关闭连接
    client.close()

    return JsonResponse({'message': '上传成功'})


@login_required(login_url='/api/auth/login')
def firmware_list(request):
    query_name = request.GET.get('search_name')
    query_vendor = request.GET.get('search_vendor')

    firmwares = FirmwareRepository.objects.all()
    if query_name:
        # 根据固件名称进行模糊搜索
        firmwares = firmwares.filter(name__icontains=query_name)

    if query_vendor:

        firmwares = firmwares.filter(vendor__icontains=query_vendor)


    page = request.GET.get('page')
    items_per_page = request.GET.get('items_per_page')

    firmwares = firmwares.order_by("id")
    paginator = Paginator(firmwares, items_per_page)

    items = paginator.get_page(page)

    total_items = paginator.count
    data_list = [{'id': item.id, 'firmware_name': item.name, 'vendor': item.vendor, 'created_at': item.created_at} for item in items]
    return JsonResponse({'firmwares': data_list, 'total_items': total_items})


@login_required(login_url='/api/auth/login')
def update_vendor(request):
    firmware_id = request.POST.get('id')
    vendor = request.POST.get('vendor')

    firmware = FirmwareRepository.objects.get(id=firmware_id)

    firmware.vendor = vendor
    firmware.save()

    return JsonResponse({'message': 'Update successful', 'id': firmware_id, 'vendor': vendor, })




@login_required(login_url='/api/auth/login')
def download_firmware(request, firmware_id):
    try:
        firmware = FirmwareRepository.objects.get(id=firmware_id)
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

        db = client['firmware_repository']

        fs = GridFS(db)

        # 获取固件文件并返回给前端
        firmware_file = fs.get(ObjectId(firmware.file_id))
        firmware_file_content = firmware_file.read()
        firmware_file_name = firmware_file.filename

        # 关闭连接
        client.close()

        response = HttpResponse(firmware_file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={quote(firmware_file_name)}'

        return response
    except ExtractFirmwareTask.DoesNotExist:
        return JsonResponse({'message': '镜像不存在'}, status=404)




@login_required(login_url='/api/auth/login')
def delete_firmware(request, task_id):
    try:
        firmware = FirmwareRepository.objects.get(id=task_id)
        file_id = firmware.file_id
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

        db = client['firmware_repository']

        fs = GridFS(db)
        fs.delete(ObjectId(file_id))

        client.close()

        firmware.delete()
        return JsonResponse({'message': '镜像已删除'})
    except ExtractFirmwareTask.DoesNotExist:
        return JsonResponse({'message': '镜像不存在'}, status=404)

