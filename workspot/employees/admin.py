from django.contrib import admin

from .models import Employee, EmployeeSkill, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "gender", "patronymic")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "patronymic",
    )
    list_filter = ("gender",)


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "skill", "level")
    list_filter = ("skill", "level")
    search_fields = ("employee__user__username", "skill__name")
