from schedule.models import Student, Group, Department


def convert_group_name_to_group_id(group_name: str) -> int:
    """Метод конвертирует имя группы в его id.

        Аргументы:
         • group_name - название группы.
        """
    group = Group.objects.get(name=group_name)
    return group.pk


def convert_department_name_to_department_id(department_name: str) -> int:
    department = Department.objects.get(name=department_name)
    return department.pk


def set_student_settings(user_id: int, first_name: str, last_name: str,
                         surname: str, department: str, course: str, group_name: str) \
        -> None:
    """Метод устанавливает группу у студента.

        Аргументы:
         • user_id - id авторизованного пользователя.
         • group_name - название группы.
    """
    student = Student.objects.get(id=user_id)
    group_id = convert_group_name_to_group_id(group_name)
    department_id = convert_department_name_to_department_id(department)

    department = Department.objects.get(id=department_id)
    group = Group.objects.get(id=group_id)

    student.first_name = first_name
    student.last_name = last_name
    student.surname = surname
    student.department = department
    student.course = int(course)
    student.group = group
    student.save()
