"""Считаем различные статистики"""
import numpy as np

from django.db.models import Count
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.home.models import Dialogs, LabelledSSI


def calculate_gold():
    """Считаем gold-разметку
    """
    gold = []
    dialogs = Dialogs.objects.exclude(is_labelled=1).annotate(num_labels=Count('labels_for_dialog'))
    labelled_dialogs = [d for d in dialogs if d.num_labels > settings.USERS_PER_SAMPLE]
    
    for d in labelled_dialogs:
        # groundedness
        yes = LabelledSSI.objects.filter(dialog=d).filter(groundedness=0).count()
        no = LabelledSSI.objects.filter(dialog=d).filter(groundedness=1).count()
        if yes == 0 and no == 0:
            continue
        groundedness_label = np.argmax(np.array([yes, no]))

        # helpfulness
        yes = LabelledSSI.objects.filter(dialog=d).filter(helpfulness=0).count()
        no = LabelledSSI.objects.filter(dialog=d).filter(helpfulness=1).count()
        if yes == 0 and no == 0:
            continue
        helpfulness_label = np.argmax(np.array([yes, no]))

        # interestingness
        yes = LabelledSSI.objects.filter(dialog=d).filter(interestingness=0).count()
        no = LabelledSSI.objects.filter(dialog=d).filter(interestingness=1).count()
        if yes == 0 and no == 0:
            continue
        interestingness_label = np.argmax(np.array([yes, no]))

        # safety
        yes = LabelledSSI.objects.filter(dialog=d).filter(safety=0).count()
        no = LabelledSSI.objects.filter(dialog=d).filter(safety=1).count()
        if yes == 0 and no == 0:
            continue
        safety_label = np.argmax(np.array([yes, no]))

        # sensibleness
        yes = LabelledSSI.objects.filter(dialog=d).filter(sensibleness=0).count()
        no = LabelledSSI.objects.filter(dialog=d).filter(sensibleness=1).count()
        if yes == 0 and no == 0:
            continue
        sensibleness_label = np.argmax(np.array([yes, no]))

        # specificity
        yes = LabelledSSI.objects.filter(dialog=d).filter(specificity=0).count()
        no = LabelledSSI.objects.filter(dialog=d).filter(specificity=1).count()
        if yes == 0 and no == 0:
            continue
        specificity_label = np.argmax(np.array([yes, no]))

        gold.append({
            'dialog': d,
            'groundedness': groundedness_label,
            'helpfulness': helpfulness_label,
            'interestingness': interestingness_label,
            'safety': safety_label,
            'sensibleness': sensibleness_label,
            'specificity': specificity_label,
        })
        d.is_labelled = 1
        d.save()
    return gold


def calculate_user_statistics():
    """Считаем метрики по пользователям"""
    gold = calculate_gold()
    User = get_user_model()
    users = User.objects.all()
    user_data = []
    max_count = 0
    for user in users:
        c = LabelledSSI.objects.filter(changed_by=user).count()
        user_data.append({
            'user': user,
            'count': c
        })
        if max_count < c:
            max_count = c
    for item in user_data:
        item.update({'count_p': int(item['count'] * 100 / (max_count + 1e-8))})
    return user_data