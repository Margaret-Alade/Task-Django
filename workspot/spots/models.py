from django.core.exceptions import ValidationError
from django.db import models

from employees.models import Employee


def validate_neighbor_spots(spot):
    """Не допускает тестировщика и разработчика за соседними столами."""
    if not spot.employee:
        return

    try:
        number = int(spot.number)
    except TypeError, ValueError:
        return

    current = spot.employee.profession
    is_current_qa = current == Employee.Profession.TESTER
    is_current_dev = current in (
        Employee.Profession.BACKEND,
        Employee.Profession.FRONTEND,
    )

    if not (is_current_qa or is_current_dev):
        return

    neighbor_numbers = [str(number - 1), str(number + 1)]
    neighbors = (
        Spot.objects.filter(number__in=neighbor_numbers)
        .exclude(pk=spot.pk)
        .select_related("employee")
    )

    for neighbor in neighbors:
        if not neighbor.employee:
            continue

        neighbor_prof = neighbor.employee.profession
        is_neighbor_qa = neighbor_prof == Employee.Profession.TESTER
        is_neighbor_dev = neighbor_prof in (
            Employee.Profession.BACKEND,
            Employee.Profession.FRONTEND,
        )

        if (is_current_qa and is_neighbor_dev) or (is_current_dev and is_neighbor_qa):
            raise ValidationError(
                f"Нельзя сажать тестировщика и разработчика за соседние столы. "
                f"Стол {spot.number} конфликтует со столом {neighbor.number}."
            )


class Spot(models.Model):
    number = models.CharField("Номер стола", max_length=20, unique=True)
    extra_info = models.TextField("Дополнительная информация", blank=True)
    employee = models.OneToOneField(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="spot"
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return f"Стол {self.number}"

    def clean(self):
        super().clean()
        validate_neighbor_spots(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
