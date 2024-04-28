from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy


class Subject(models.Model):
    """Модель учебного предмета.

    Атрибуты:
        • name (str): Название учебного предмета.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Department(models.Model):
    """Модель отдела.

    Атрибуты:
        • name (str): Название кафедры.
        • subjects (ManyToManyField): Связь многие ко многим с предметами.
    """
    name = models.CharField(max_length=50)
    subjects = models.ManyToManyField('Subject', related_name='department')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'


class Group(models.Model):
    """Модель группы.

    Атрибуты:
        • name (str): Название группы.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Student(AbstractUser):
    """Модель студента.

    Атрибуты:
        • surname (str): Фамилия студента.
        • group (ForeignKey): Связь с моделью Группа.
        • department (ForeignKey): Связь с моделью Кафедра.
        • course (int): Курс студента.
    """
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
        """Метод для получения URL аватара студента."""
        avatar_url = SocialAccount.objects.filter(user=self).get().extra_data[
            'picture']
        return avatar_url

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(models.Model):
    """Модель учителя.

    Атрибуты:
        • first_name (str): Имя учителя.
        • last_name (str): Фамилия учителя.
        • surname (str): Отчество учителя.
        • subjects (ForeignKey): Связь с моделью Предмет.
    """
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)
    surname = models.CharField(max_length=50,blank=True)
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
    """Модель урока.

    Атрибуты:
        • week (str): Неделя(четная или нечетная).
        • group (ForeignKey): Связь с моделью Группа.
        • period (str): На каком часу проходит урок.
        • teacher (ForeignKey): Учитель, который проводит урок.
        • day (str): День недели, в который запланирован урок.
        • audience (str): Номер аудитории, где проходит урок.
        • subject (ForeignKey): Предмет урока.
    """
    class WeekChoice(models.TextChoices):
        FIRST_WEEK = 'FIRST_WEEK', gettext_lazy('ПЕРВАЯ')
        SECOND_WEEK = 'SECOND_WEEK', gettext_lazy('ВТОРАЯ')

    class DoublePeriodChoice(models.TextChoices):
        FIRST_PERIOD = 'FP', gettext_lazy('1-2')
        SECOND_PERIOD = 'SP', gettext_lazy('3-4')
        THIRD_PERIOD = 'FR', gettext_lazy('5-6')
        FOURTH_PERIOD = 'FH', gettext_lazy('7-8')
        FIFTH_PERIOD = 'FF', gettext_lazy('9-10')
        SIXTH_PERIOD = 'SX', gettext_lazy('11-12')

    class DayChoice(models.TextChoices):
        MONDAY = 'MN', gettext_lazy('Понедельник')
        TUESDAY = 'TU', gettext_lazy('Вторник')
        WEDNESDAY = 'WD', gettext_lazy('Среда')
        THURSDAY = 'TH', gettext_lazy('Четверг')
        FRIDAY = 'FR', gettext_lazy('Пятница')
        SATURDAY = 'ST', gettext_lazy('Суббота')

    week = models.CharField(max_length=11, choices=WeekChoice.choices, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lesson', blank=True)
    period = models.CharField(choices=DoublePeriodChoice.choices, max_length=5, blank=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        related_name='lesson', blank=True
    )
    day = models.CharField(choices=DayChoice.choices, max_length=5, blank=True)
    audience = models.CharField(max_length=5, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True)
    pdf_file = models.FileField(upload_to="upload_file/")
    crud_file = models.FileField(upload_to='tables', blank=True)

    def __str__(self):
        return self.subject.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Schedule(models.Model):
    pdf_file = models.FileField(upload_to='upload_file')


