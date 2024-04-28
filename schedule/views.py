import csv
import json
import os
import time

import camelot
import convertio
import requests
import tabula
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from schedule.models import Lesson, Group, Teacher, Subject, Schedule

from .forms import UploadFileForm


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




def create_lessons_from_table(html_table,pdf_file):
    lessons = []
    soup = BeautifulSoup(html_table, 'html.parser')
    rows = soup.find_all('tr')
    week = ''.join(rows[1].text.strip().split())[:-6]
    for row in rows[2:]:  # Skip the header row
        columns = row.find_all('td')
        for column_idx in range(8, 11):
            if columns[column_idx].text:

                day = columns[1].text.replace('\\r', '')
                period = columns[6].text.strip()
                subject = columns[column_idx].text.strip().split('\\r')[0]
                teacher = columns[column_idx].text.strip().split('\\r')[-1].split()[0]
                # audience = columns[10].text.strip()


                subject, _ = Subject.objects.get_or_create(name=subject)
                teacher, _ = Teacher.objects.get_or_create(last_name=teacher,subjects=subject)
                group = ['ВХТ-351', 'ВХЭ-356', 'ВХТ-355'][column_idx-8]
                print(day)
                lesson = Lesson(
                    week=week,  # Assuming all lessons are on the first week
                    group=Group.objects.get(name=group),
                    period=period,
                    teacher=teacher,  # Update with actual teacher name
                    day=day,
                    audience='b-303',
                    subject=subject,  # Update with actual subject name
                    pdf_file=pdf_file
                )

                if lesson not in Lesson.objects.all():
                    lessons.append(lesson)

    Lesson.objects.bulk_create(lessons)  # Save all lessons to the database at once


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            pdf_instance = Schedule(pdf_file=pdf_file)  # Save the file in the Schedule model
            pdf_instance.save()

            df = tabula.read_pdf(pdf_file, pages="all", stream=True, lattice=True, multiple_tables=True)[0]
            if len(df) > 0:
                data = df.to_html(na_rep='', index=False)
                create_lessons_from_table(data, pdf_file)
                return render(request, 'schedule/upload_file.html', {'data': data, 'form': form})

    else:
        form = UploadFileForm()
        return render(request, 'schedule/upload_file.html', {'form': form})


def pdfs(request):
    pdf_files = list(Lesson.objects.values_list('pdf_file', flat=True).distinct())
    return render(request, 'schedule/pdf/pdfs.html', {'pdf_files': pdf_files})


def pdf_detail(request, pdf_detail):
    lessons_with_pdf = Lesson.objects.filter(pdf_file=pdf_detail)

    if lessons_with_pdf.exists():
        pdf = lessons_with_pdf[0].pdf_file
        crud = lessons_with_pdf[0].crud_file
        teachers = Teacher.objects.all()
        subjects = Subject.objects.all()
        groups = Group.objects.all()
        crud_table = []

        id_teacher_mapping = {teacher.id: teacher for teacher in teachers}
        id_subject_mapping = {subject.id: subject.name for subject in subjects}
        id_group_mapping = {group.id: group.name for group in groups}

        storage = FileSystemStorage()
        crud_path = storage.path(crud.name)

        with open(crud_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header of the file
            for row in csv_reader:
                row_values = []  # Reset row_values for each row
                for index, value in enumerate(row):

                    if index not in [0, 8, 9]:
                        if index == 4 and int(value) in id_teacher_mapping:
                            row_values.append(id_teacher_mapping[int(value)])
                        elif index == 7 and int(value) in id_subject_mapping:
                            row_values.append(id_subject_mapping[int(value)])
                        elif index == 2 and int(value) in id_group_mapping:
                            row_values.append(id_group_mapping[int(value)])
                        else:
                            row_values.append(value)
                crud_table.append(row_values)

        return render(request, 'schedule/pdf/pdf_detail.html', {'crud': crud_table, 'pdf': pdf})
    else:
        return HttpResponse('Нет такого пдф файла')
