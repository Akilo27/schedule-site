from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from schedule.models import Group, Department
from user_profile.services.profile_settings import set_student_settings

class ProfileSettingsView(View):
    def get(self, request):
        all_groups = Group.objects.all()
        all_department = Department.objects.all()
        return render(
            request, 'profile/user_profile.html', context={
                'user': request.user,
                'all_groups': all_groups,
                'all_department': all_department
            }
        )

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def post(request):
        response = request.POST
        user = request.user  # Получаем пользователя через request

        first_name = response.get('first_name')
        last_name = response.get('last_name')
        surname = response.get('surname')
        department = response.get('department')
        course = response.get('course')
        group_name = response.get('group')

        set_student_settings(
            user_id=user.id, first_name=first_name,
            last_name=last_name, surname=surname,
            department=department, course=course, group_name=group_name
        )

        return HttpResponseRedirect(reverse('profile_settings'))
