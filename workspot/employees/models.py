from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile"
    )
    gender = models.CharField(
        max_length=1, choices=[("M", "Мужской"), ("F", "Женский")], blank=True
    )
    patronymic = models.CharField("Отчество", max_length=100, blank=True)
    skills = models.ManyToManyField(
        Skill, through="EmployeeSkill", related_name="employees"
    )
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 11)]
    )

    def __str__(self):
        return f"{self.employee} — {self.skill} ({self.level})"


@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)
