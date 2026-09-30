from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Employee


def home(request):
    """Главная: описание проекта + карточки сотрудников."""
    employees = Employee.objects.select_related("user").prefetch_related("skills")[:6]
    context = {
        "employees": employees,
        "page_title": "Добро пожаловать в Workspot",
    }
    return render(request, "home.html", context)


def employee_list(request):
    """Список всех сотрудников."""
    employees = Employee.objects.select_related("user").prefetch_related("skills")
    context = {
        "employees": employees,
        "page_title": "Сотрудники",
    }
    return render(request, "employees/list.html", context)


@login_required
def employee_detail(request, pk):
    """Подробная карточка сотрудника. Только для авторизованных."""
    employee = get_object_or_404(
        Employee.objects.select_related("user").prefetch_related("skill_levels__skill"),
        pk=pk,
    )
    context = {
        "employee": employee,
        "page_title": f"{employee.user.get_full_name() or employee.user.username}",
    }
    return render(request, "employees/detail.html", context)
