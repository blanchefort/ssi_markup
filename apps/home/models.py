# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Dialogs(models.Model):
    """Диалоги для SSI-разметки
    """
    LABELING_TYPES = (
        (0, 'Не размечен'),
        (1, 'Размечен'),
    )

    prev_query_text = models.TextField(verbose_name='История, пользователь')
    prev_response_text = models.TextField(verbose_name='История, бот')
    query_text = models.TextField(verbose_name='Реплика пользователя')
    response_text = models.TextField(verbose_name='Ответ бота для разметки')

    is_labelled = models.PositiveSmallIntegerField(
        verbose_name='Отметка о разметке',
        default=0,
        null=True,
        choices=LABELING_TYPES
    )

    def __str__(self):
        return str(self.response_text)

    class Meta:
        verbose_name = 'Реплика для разметки'
        verbose_name_plural = 'Реплики для разметки'


class LabelledSSI(models.Model):
    """Метки размеченных текстов
    """
    LABELS = (
        (0, 'Yes'),
        (1, 'No'),
        (2, 'May be'),
    )

    dialog = models.ForeignKey(
        Dialogs,
        on_delete=models.SET_NULL,
        related_name='labels_for_dialog',
        default=None,
        null=True)
    
    groundedness = models.PositiveSmallIntegerField(
        verbose_name='Groundedness',
        default=0,
        null=True,
        choices=LABELS
    )

    helpfulness = models.PositiveSmallIntegerField(
        verbose_name='Helpfulness',
        default=0,
        null=True,
        choices=LABELS
    )

    interestingness = models.PositiveSmallIntegerField(
        verbose_name='Interestingness',
        default=0,
        null=True,
        choices=LABELS
    )

    safety = models.PositiveSmallIntegerField(
        verbose_name='Safety',
        default=0,
        null=True,
        choices=LABELS
    )

    sensibleness = models.PositiveSmallIntegerField(
        verbose_name='Sensibleness',
        default=0,
        null=True,
        choices=LABELS
    )

    specificity = models.PositiveSmallIntegerField(
        verbose_name='Specificity',
        default=0,
        null=True,
        choices=LABELS
    )

    changed_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        related_name='labels_for_user',
        default=None,
        null=True)

    labeling_time = models.DateTimeField(
        default=timezone.now,
        blank=True,
        verbose_name='Дата разметки')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Метки реплики бота'
        verbose_name_plural = 'Метки реплик бота'
