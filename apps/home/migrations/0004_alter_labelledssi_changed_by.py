# Generated by Django 3.2.11 on 2022-05-10 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_auto_20220510_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelledssi',
            name='changed_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='labels_for_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
