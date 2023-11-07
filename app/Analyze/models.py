from django.db import models
from django.utils import timezone


class AnalyzeFirmwareTask(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('analyzing', '正在分析'),
        ('completed', '已完成'),
         ('failed', '失败')
    ]

    firmware_name = models.CharField(max_length=100)  # 存储固件名称
    created_at = models.DateTimeField(default=timezone.now)
    file_id = models.CharField(max_length=100)  # 存储 GridFS 文件 ID
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    firmware_result = models.JSONField(null=True)  # 存储固件分析结果的 JSON 数据

    def __str__(self):
        return f"分析任务 ID: {self.id}, 状态: {self.status}, 所属任务: {self.firmware_task}"
