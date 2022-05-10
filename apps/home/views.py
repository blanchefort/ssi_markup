# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import json
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from django.db.models import Count

from apps.home.forms import AddDialog, UploadDialogs
from apps.home.models import Dialogs, LabelledSSI
from apps.home.scores import calculate_user_statistics


@login_required(login_url="/login/")
def index(request):
    """Стартовая страница"""
    if request.user.is_superuser:
        sample_count = Dialogs.objects.count()
        dialogs = Dialogs.objects.exclude(is_labelled=1).annotate(num_labels=Count('labels_for_dialog'))
        partly_completed = 0
        for d in dialogs:
            if d.num_labels > 0:
                partly_completed += 1
        fully_completed = Dialogs.objects.filter(is_labelled=1).count()
        context = {
            'segment': 'index',
            'sample_count': sample_count, # Размер выборки
            'partly_completed': partly_completed, # Частично размечено
            'fully_completed': fully_completed, # Полностью размечено
            'partly_completed_p': int(partly_completed * 100 / (sample_count + 1e-8)), # %
            'fully_completed_p': int(fully_completed * 100 / (sample_count + 1e-8)), # %
            'user_data': calculate_user_statistics()
        }
    else:
        #user interface
        marked_count = LabelledSSI.objects.filter(changed_by=request.user).count()
        context = {
            'segment': 'index',
            'marked_count': marked_count,
        }
    return TemplateResponse(request, 'layouts/index.html', context=context)


@login_required(login_url="/login/")
def rules(request):
    """Правила разметки"""
    context = {
        'segment': 'rules',
    }
    return TemplateResponse(request, 'layouts/rules.html', context=context)


@login_required(login_url="/login/")
def markup(request):
    """Разметка"""
    if request.method == 'POST':
        try:
            LabelledSSI.objects.create(
                dialog=Dialogs.objects.get(pk=int(request.POST['item_id'])),
                groundedness = request.POST.get('groundedness', 0),
                helpfulness = request.POST.get('helpfulness', 0),
                interestingness = request.POST.get('interestingness', 0),
                safety = request.POST.get('safety', 0),
                specificity = request.POST.get('specificity', 0),
                sensibleness = request.POST.get('sensibleness', 0),
                changed_by=request.user,
                labeling_time=timezone.now(),
            )
        except:
            messages.error(request, 'Заполните все метки корректно!')

    sample = Dialogs.objects.exclude(is_labelled=1).exclude(labels_for_dialog__changed_by=request.user).first()

    context = {
        'segment': 'markup',
        'sample': sample,
    }
    return TemplateResponse(request, 'layouts/markup.html', context=context)


@login_required(login_url="/login/")
def upload(request):
    """Разметка"""
    add_dialog_form = AddDialog()
    upload_dialogs_form = UploadDialogs()
    if request.method == 'POST':
        if 'file' in request.FILES:
            upload_dialogs_form = UploadDialogs(request.POST, request.FILES)
            if upload_dialogs_form.is_valid() and request.FILES['file']:
                file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                filename = os.path.join(settings.MEDIA_ROOT, filename)

                try:
                    with open(filename) as fp:
                        data = json.load(fp)
                    for item in data:
                        Dialogs.objects.create(
                        prev_query_text=item['prev_query_text'],
                        prev_response_text=item['prev_response_text'],
                        query_text=item['query_text'],
                        response_text=item['response_text']
                    )
                    messages.success(request, 'Датасет добавлен')
                except:
                    messages.error(request, 'Проверьте корректность json-файла')
                fs.delete(filename)
        else:
            add_dialog_form = AddDialog(request.POST)
            prev_query_text = request.POST.get('prev_query_text', '').strip()
            prev_response_text = request.POST.get('prev_response_text', '').strip()
            query_text = request.POST.get('query_text', '').strip()
            response_text = request.POST.get('response_text', '').strip()
            if len(query_text) > 0 and len(response_text) > 0:
                Dialogs.objects.create(
                    prev_query_text=prev_query_text,
                    prev_response_text=prev_response_text,
                    query_text=query_text,
                    response_text=response_text
                )
                messages.success(request, 'Сэмпл добавлен')
            else:
                messages.error(request, 'Заполните поля')

    context = {
        'segment': 'upload',
        'add_dialog_form': add_dialog_form,
        'upload_dialogs_form': upload_dialogs_form
    }
    return TemplateResponse(request, 'layouts/upload.html', context=context)
