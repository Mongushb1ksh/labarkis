from django.contrib import admin

from .forms import UserProfileForm
from .models import Question, Choice, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

    def avatar_display(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" />')
        return 'No avatar'
    avatar_display.short_description = 'Avatar'  # Название столбца в админке


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Question, QuestionAdmin)
