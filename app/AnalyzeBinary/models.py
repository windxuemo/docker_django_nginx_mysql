
from django.db import models
from django.utils import timezone


class AnalyzeBinaryTask(models.Model):
    binary_file_name = models.CharField(max_length=255)
    binary_file_id = models.CharField(max_length=255)
    analysis_status = models.CharField(max_length=50)
    analysis_result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.binary_file_name

