# Generated by Django 4.2.3 on 2023-07-18 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_quiz', to=settings.AUTH_USER_MODEL),
        ),
    ]