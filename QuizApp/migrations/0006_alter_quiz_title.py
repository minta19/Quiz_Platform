# Generated by Django 4.2.3 on 2023-07-19 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0005_remove_quizanswers_score_quizquestions_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]