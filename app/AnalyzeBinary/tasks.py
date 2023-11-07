#!/usr/bin/env python
# coding=utf-8

from celery import Celery

def celery_send_task(task_id):
    app = Celery()
    app.config_from_object('celeryconfig')
    # 发送任务到远程机器
    result = app.send_task('tasks.task_analyze_binary', args=[task_id], queue='analyze_binary')

