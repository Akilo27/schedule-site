from django.contrib import admin

from schedule.models import Group, Student, Subject, Department, Teacher, Lesson


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
class Lesson(admin.ModelAdmin):
    list_display = ('id', 'period', 'subject', 'week', 'teacher', 'audience',)
