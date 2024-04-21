# Generated by Django 5.0.4 on 2024-04-21 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_lesson_day_alter_lesson_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='day',
            field=models.CharField(choices=[('MN', 'Понедельник'), ('TU', 'Вторник'), ('WD', 'Среда'), ('TH', 'Четверг'), ('FR', 'Пятница'), ('ST', 'saturday')], max_length=5),
        ),
    ]
