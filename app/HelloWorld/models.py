# -*- coding: utf-8 -*-

from django.db import models

class ExtractFirmwareTask(models.Model):
    STATUS_CHOICES = [
        ('unpacked', '未解包'),
        ('unpacking', '正在解包'),
        ('completed', '已完成'),
    ]

    file_id = models.CharField(max_length=100)  # 存储 GridFS 文件 ID
    firmware_name = models.CharField(max_length=100)  # 存储固件名称
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpacked')
    extracted_file_id = models.CharField(max_length=100, null=True)  # 存储 GridFS 文件 ID

    def __str__(self):
        return f'任务 ID: {self.id}, 状态: {self.status}, 固件名称: {self.firmware_name}'

