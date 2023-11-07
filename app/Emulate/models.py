from django.db import models
from django.utils import timezone


class EmulateFirmwareTask(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('emulating', '正在分析'),
        ('completed', '已完成'),
        ('terminating', '终止中'),
        ('terminated', '已终止'),
         ('failed', '失败')
    ]

    firmware_name = models.CharField(max_length=255)  # 存储固件名称
    file_id = models.CharField(max_length=100)  # 存储 GridFS 文件 ID
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    web_ip = models.CharField(max_length=45)
    nginx_ip = models.CharField(max_length=45)
    pid = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"分析任务 ID: {self.id}, 状态: {self.status}, 所属任务: {self.firmware_name}"
