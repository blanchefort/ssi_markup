from django import forms
from apps.home.models import Dialogs


class AddDialog(forms.ModelForm):
    """Добавление одиночного сэмпла"""
    class Meta:
        model = Dialogs
        fields = ('prev_query_text', 'prev_response_text', 'query_text', 'response_text',)


class UploadDialogs(forms.Form):
    """Форма для загрузки файла с текстами
    """
    file = forms.FileField(label='CSV-файл с текстами')
