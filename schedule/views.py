from django.shortcuts import render
from django.views import View

from schedule.models import Lesson, Group, Teacher


# Create your views here.


class ScheduleView(View):
    def get(self, request):
        lessons = Lesson.objects.all()
        groups = Group.objects.all()
        teachers = Teacher.objects.all()
        context = {
            'lessons': lessons,
            'groups': groups,
            'teachers': teachers
        }
        return render(request, 'schedule/schedule.html', context=context)

    def post(self, request):
        r = request.POST
        groups = Group.objects.all()
        teachers = Teacher.objects.all()

        group_id = r.get('group_id')
        lesson_id = r.get('lesson_id')
        teacher_id = r.get('teacher_id')

        lessons = Lesson.objects.filter(teacher_id=teacher_id, group_id=group_id)
        context = {
            'lessons': lessons,
            'groups': groups,
            'teachers': teachers
        }
        return render(request, 'schedule/schedule.html', context=context)


def sidebar(request):
    return render(request, 'includes/sidebar.html')
