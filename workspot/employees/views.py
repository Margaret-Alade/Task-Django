from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Employee


def home(request):
    """Главная: описание проекта + карточки сотрудников."""
    employees = (
        Employee.objects.select_related("user")
        .prefetch_related("skill_levels__skill", "images")
        .order_by("-hire_date")
        .filter(hire_date__isnull=False)[:4]
    )
    context = {
        "employees": employees,
        "total_employees": Employee.objects.count(),
        "page_title": "Добро пожаловать в Workspot",
    }
    return render(request, "home.html", context)


def employee_list(request):
    """Список всех сотрудников с пагинацией по 10 на странице."""
    employees_qs = (
        Employee.objects.select_related("user")
        .prefetch_related("skill_levels__skill", "images")
        .order_by("user__last_name", "user__first_name")
    )

    paginator = Paginator(employees_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "page_title": "Сотрудники",
    }
    return render(request, "employees/list.html", context)


@login_required
def employee_detail(request, pk):
    """Подробная карточка сотрудника. Только для авторизованных."""
    employee = get_object_or_404(
        Employee.objects.select_related("user", "spot").prefetch_related(
            "skill_levels__skill", "images"
        ),
        pk=pk,
    )

    images = list(employee.images.all())
    main_image = images[0] if images else None
    gallery_images = images[1:]  # все, кроме первого

    context = {
        "employee": employee,
        "main_image": main_image,
        "gallery_images": gallery_images,
        "page_title": f"{employee.user.get_full_name() or employee.user.username}",
    }
    return render(request, "employees/detail.html", context)
