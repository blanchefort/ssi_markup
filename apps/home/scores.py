"""Считаем различные статистики"""
import numpy as np
from sklearn.metrics import cohen_kappa_score

from django.db.models import Count
from django.conf import settings
from django.contrib.auth import get_user_model


from apps.home.models import Dialogs, LabelledSSI


def calculate_gold():
    """Считаем gold-разметку
    """
    gold = []
    dialogs = Dialogs.objects.annotate(num_labels=Count('labels_for_dialog'))
    labelled_dialogs = [d for d in dialogs if d.num_labels >= settings.USERS_PER_SAMPLE]

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


def kappa_score(user, gold):
    """Считаем каппу Коена для пользователя"""
    selected_target, selected_gold = [], []
    for y in gold:
        if LabelledSSI.objects.filter(changed_by=user).filter(dialog=y['dialog']).count() == 0:
            continue
        item = LabelledSSI.objects.filter(changed_by=user).filter(dialog=y['dialog']).first()
        if (item.groundedness == 2 or \
            item.helpfulness == 2 or \
            item.interestingness == 2 or \
            item.safety == 2 or \
            item.sensibleness == 2 or \
            item.specificity == 2):
            continue
        selected_target.append(item)
        selected_gold.append(y)

    if len(selected_target) < 1:
        return 0

    counter = 6
    #groundedness
    groundedness = cohen_kappa_score(
        [i.groundedness for i in selected_target],
        [i['groundedness'] for i in selected_gold])
    if groundedness == np.nan:
        groundedness = 1e-8
        counter -= 1
    #helpfulness
    helpfulness = cohen_kappa_score(
        [i.helpfulness for i in selected_target],
        [i['helpfulness'] for i in selected_gold])
    if helpfulness == np.nan:
        helpfulness = 1e-8
        counter -= 1
    #interestingness
    interestingness = cohen_kappa_score(
        [i.interestingness for i in selected_target],
        [i['interestingness'] for i in selected_gold])
    if interestingness == np.nan:
        interestingness = 1e-8
        counter -= 1
    #safety
    safety = cohen_kappa_score(
        [i.safety for i in selected_target],
        [i['safety'] for i in selected_gold])
    if safety == np.nan:
        safety = 1e-8
        counter -= 1
    #sensibleness
    sensibleness = cohen_kappa_score(
        [i.sensibleness for i in selected_target],
        [i['sensibleness'] for i in selected_gold])
    if sensibleness == np.nan:
        sensibleness = 1e-8
        counter -= 1
    #specificity
    specificity = cohen_kappa_score(
        [i.specificity for i in selected_target],
        [i['specificity'] for i in selected_gold])
    if specificity == np.nan:
        specificity = 1e-8
        counter -= 1
    #average kappa
    avg_kappa = (groundedness + helpfulness + interestingness + safety + sensibleness + specificity) / counter

    return  avg_kappa


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
        kappa = kappa_score(item['user'], gold)

        if kappa < 0:
            kappa_p = 0
        else:
            kappa_p = kappa

        kappa_p = int(kappa_p * 100)

        item.update({'kappa': kappa})
        item.update({'kappa_p': kappa_p})
    return user_data



