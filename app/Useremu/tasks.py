#!/usr/bin/env python
# coding=utf-8

from celery import Celery

def celery_send_task(task_id, cmd_args):
    app = Celery()
    app.config_from_object('celeryconfig')
    # 发送任务到远程机器
    result = app.send_task('tasks.task_user_emulate_bin', args=[task_id, cmd_args], queue='user_emulate')

def celery_kill_task(task_id, pid):
    app = Celery()
    app.config_from_object('celeryconfig')
    # 发送任务到远程机器
    result = app.send_task('tasks.task_terminate_process', args=[task_id, pid], queue='user_emulate')
