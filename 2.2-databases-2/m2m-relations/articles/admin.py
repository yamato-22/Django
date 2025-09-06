from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_main_tag = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                count_main_tag += 1
        if count_main_tag != 1:
            raise ValidationError('Нужно указать один основной тег!')
            # В form.cleaned_data словарь с данными
            # каждой отдельной формы, которые можно проверить
            # вызовом исключения ValidationError можно указываем админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
            # затем вызываем базовый код переопределяемого метода super().clean()
        return super().clean()

class RelationshipInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline,]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']