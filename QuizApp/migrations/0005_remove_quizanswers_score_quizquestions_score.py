# Generated by Django 4.2.3 on 2023-07-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0004_alter_quiz_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizanswers',
            name='score',
        ),
        migrations.AddField(
            model_name='quizquestions',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
