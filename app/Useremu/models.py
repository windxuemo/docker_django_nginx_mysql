from django.db import models
from django.utils import timezone


class UserEmulateTask(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('terminatng', '正在终止'),
        ('listening', '正在分析'),
        ('closed', '已完成'),
         ('failed', '失败')
    ]

    binary_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    binary_file_id = models.CharField(max_length=100)  # 存储 GridFS 文件 ID
    rootfs_name = models.CharField(max_length=255)
    rootfs_file_id = models.CharField(max_length=100)  # 存储 GridFS 文件 ID
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    debug_ip = models.CharField(max_length=45, null=True, blank=True)
    debug_port = models.IntegerField(null=True, blank=True)
    pid = models.IntegerField(null=True, blank=True)
