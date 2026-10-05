import os
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Employee(models.Model):
    class Profession(models.TextChoices):
        TESTER = "QA", "Тестировщик"
        BACKEND = "BE", "Бэкенд-разработчик"
        FRONTEND = "FE", "Фронтенд-разработчик"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile"
    )
    profession = models.CharField(
        "Профессия",
        max_length=2,
        choices=Profession.choices,
        blank=True,
    )
    gender = models.CharField(
        max_length=1, choices=[("M", "Мужской"), ("F", "Женский")], blank=True
    )
    patronymic = models.CharField("Отчество", max_length=100, blank=True)
    skills = models.ManyToManyField(
        Skill, through="EmployeeSkill", related_name="employees"
    )
    description = models.TextField("Описание", blank=True)
    hire_date = models.DateField(
        "Дата приёма на работу",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    @property
    def experience_days(self):
        """Стаж работы в компании в днях."""
        if not self.hire_date:
            return None
        return (date.today() - self.hire_date).days

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="skill_levels"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 11)]
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудника"

    def __str__(self):
        return f"{self.employee} — {self.skill} ({self.level})"


def employee_image_upload_to(instance, filename):
    return f"employees/{instance.employee_id}/{filename}"


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField("Изображение", upload_to=employee_image_upload_to)
    order = models.PositiveSmallIntegerField("Порядковый номер", default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Изображения сотрудников"

    def __str__(self):
        return f"{self.employee} — изображение #{self.order}"


@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_delete, sender=EmployeeImage)
def delete_image_file(sender, instance, **kwargs):
    if not instance.image:
        return

    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

    image_dir = os.path.dirname(instance.image.path)
    if os.path.isdir(image_dir) and not os.listdir(image_dir):
        os.rmdir(image_dir)
