from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from schedule.models import Group, Department
from user_profile.services.profile_settings import set_student_settings


# Create your views here.

class ProfileSettingsView(View):
    def get(self, request):
        all_groups = Group.objects.all()  # Получаем список всех групп
        all_department = Department.objects.all()  # Получаем список всех кафедр
        return render(
            request, 'profile/user_profile.html', context={
                'user': request.user,
                'all_groups':
                    all_groups,
                'all_department': all_department
            }
        )

    def post(self, request):
        response = request.POST

        first_name = response.get('first_name')  # Получаем введенное имя из формы
        last_name = response.get('last_name')  # Получаем введенную фамилию из формы
        surname = response.get('surname')  # Получаем введенное отчество из формы
        department = response.get('department')  # Получаем выбранную кафедру из формы
        course = response.get('course')  # Получаем выбранный курс из формы
        group_name = response.get('group')  # Получаем выбранную группу из формы

        set_student_settings(
            user_id=request.user.id, first_name=first_name,
            last_name=last_name, surname=surname,
            department=department, course=course, group_name=group_name
        )

        return HttpResponseRedirect(reverse('profile_settings'))
