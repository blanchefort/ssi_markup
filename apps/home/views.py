# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import json
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone

from apps.home.forms import AddDialog, UploadDialogs
from apps.home.models import Dialogs, LabelledSSI


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


#########



@login_required(login_url="/login/")
def index(request):
    """Стартовая страница"""
    marked_count = LabelledSSI.objects.filter(changed_by=request.user).count()
    context = {
        'segment': 'index',
        'marked_count': marked_count
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
                start_labeling=timezone.now(),
                end_labeling=timezone.now(),
            )
        except:
            messages.error(request, 'Заполните все метки корректно!')

    sample = Dialogs.objects.exclude(labels_for_dialog__changed_by=request.user).first()

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
