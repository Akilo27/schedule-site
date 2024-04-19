from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Department(models.Model):
    name = models.CharField(max_length=50)
    subjects = models.ManyToManyField('Subject', related_name='groups')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Student(AbstractUser):
    # Добавьте свои дополнительные поля
    surname = models.CharField(max_length=50, blank=True)
    group = models.ForeignKey(
        'Group', on_delete=models.CASCADE, related_name='student',
        null=True, blank=True
    )
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE,
        related_name='student', null=True, blank=True
    )
    course = models.IntegerField(null=True, blank=True)

    def get_avatar(self):
        avatar_url = SocialAccount.objects.filter(user=self).get().extra_data[
            'picture']
        return avatar_url

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    subjects = models.ForeignKey(
        to='Subject',
        on_delete=models.CASCADE,
        related_name='teacher',
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Lesson(models.Model):
    class WeekChoice(models.TextChoices):
        FIRST_WEEK = 'FW', gettext_lazy('Первая')
        SECOND_WEEK = 'SW', gettext_lazy('Вторая')

    class DoublePeriodChoice(models.TextChoices):
        FIRST_PERIOD = 'FP', gettext_lazy('1-2')
        SECOND_PERIOD = 'SP', gettext_lazy('3-4')
        THIRD_PERIOD = 'FR', gettext_lazy('5-6')
        FOURTH_PERIOD = 'FH', gettext_lazy('7-8')
        FIFTH_PERIOD = 'FF', gettext_lazy('9-10')
        SIXTH_PERIOD = 'SX', gettext_lazy('11-12')

    week = models.CharField(max_length=7, choices=WeekChoice.choices)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='lesson')
    period = models.CharField(choices=DoublePeriodChoice.choices, max_length=5)
    teacher = models.ForeignKey(
        'Teacher', on_delete=models.CASCADE,
        related_name='lesson'
    )
    audience = models.CharField(max_length=5)
    date = models.DateField(null=True, blank=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
