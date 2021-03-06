# Generated by Django 3.2.11 on 2022-05-10 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labelledssi',
            name='label',
        ),
        migrations.AddField(
            model_name='labelledssi',
            name='groundedness',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Yes'), (1, 'No'), (2, 'May be')], default=0, null=True, verbose_name='Groundedness'),
        ),
        migrations.AddField(
            model_name='labelledssi',
            name='helpfulness',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Yes'), (1, 'No'), (2, 'May be')], default=0, null=True, verbose_name='Helpfulness'),
        ),
        migrations.AddField(
            model_name='labelledssi',
            name='interestingness',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Yes'), (1, 'No'), (2, 'May be')], default=0, null=True, verbose_name='Interestingness'),
        ),
        migrations.AddField(
            model_name='labelledssi',
            name='safety',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Yes'), (1, 'No'), (2, 'May be')], default=0, null=True, verbose_name='Safety'),
        ),
        migrations.AddField(
            model_name='labelledssi',
            name='sensibleness',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Yes'), (1, 'No'), (2, 'May be')], default=0, null=True, verbose_name='Sensibleness'),
        ),
        migrations.AddField(
            model_name='labelledssi',
            name='specificity',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Yes'), (1, 'No'), (2, 'May be')], default=0, null=True, verbose_name='Specificity'),
        ),
    ]
