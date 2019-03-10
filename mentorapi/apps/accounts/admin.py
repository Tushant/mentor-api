from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import (User, Profile, Experience, Skill,
                                  Education, Language, Achievement)


class ExtendedUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff']
    list_editable = ['first_name', 'last_name', 'role']

    class Meta:
        model = User


class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile


class ExperienceAdmin(admin.ModelAdmin):
    class Meta:
        model = Experience


class SkillAdmin(admin.ModelAdmin):
    class Meta:
        model = Skill


class LanguageAdmin(admin.ModelAdmin):
    class Meta:
        model = Language


class EducationAdmin(admin.ModelAdmin):
    class Meta:
        model = Education


class AchievementAdmin(admin.ModelAdmin):
    class Meta:
        model = Achievement


admin.site.register(User, ExtendedUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Achievement, AchievementAdmin)
