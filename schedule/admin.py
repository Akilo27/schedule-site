import os

import pandas as pd
from django.contrib import admin

from schedule.models import Group, Student, Subject, Department, Teacher, Lesson,Schedule


# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'group', 'department', 'course')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'subjects')
    list_display_links = ('first_name', 'last_name', 'surname')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'period', 'subject', 'week', 'teacher', 'audience',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        file_name = f'{obj.pdf_file.name[:-12]}.pdf'
        file_path = os.path.join('media/', file_name)

        if os.path.exists(file_path):
            os.remove(obj.pdf_file.path)
            obj.pdf_file = file_path

        # Генерирование таблицы CRUD
        lessons = Lesson.objects.filter(week=obj.week)
        df = pd.DataFrame(lessons.values())

        file_name = f"lessons_week_{obj.week}.crud"
        file_path = os.path.join('media/tables', file_name)

        if os.path.exists(file_path):
            obj.crud_file = file_path[6:]
            obj.save()
            existing_df = pd.read_csv(file_path)
            df = pd.concat([existing_df, df], ignore_index=True, sort=False)
            df.drop_duplicates(inplace=True)

        df.to_csv(file_path, index=False)

@admin.register(Schedule)
class LessonAdmin(admin.ModelAdmin):
    pass




