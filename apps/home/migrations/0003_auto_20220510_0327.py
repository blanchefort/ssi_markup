# Generated by Django 3.2.11 on 2022-05-10 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220510_0309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dialogs',
            old_name='bot_utt_2',
            new_name='response_text',
        ),
        migrations.RemoveField(
            model_name='dialogs',
            name='bot_utt_1',
        ),
        migrations.RemoveField(
            model_name='dialogs',
            name='user_utt_1',
        ),
        migrations.RemoveField(
            model_name='dialogs',
            name='user_utt_2',
        ),
        migrations.AddField(
            model_name='dialogs',
            name='prev_query_text',
            field=models.TextField(default=0, verbose_name='История, пользователь'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dialogs',
            name='prev_response_text',
            field=models.TextField(default=0, verbose_name='История, бот'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dialogs',
            name='query_text',
            field=models.TextField(default=0, verbose_name='Реплика пользователя'),
            preserve_default=False,
        ),
    ]
