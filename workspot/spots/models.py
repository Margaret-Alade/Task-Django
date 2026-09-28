from django.db import models

from employees.models import Employee


class Spot(models.Model):
    number = models.CharField("Номер стола", max_length=20, unique=True)
    extra_info = models.TextField("Дополнительная информация", blank=True)
    employee = models.OneToOneField(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="spot"
    )

    def __str__(self):
        return f"Стол {self.number}"
