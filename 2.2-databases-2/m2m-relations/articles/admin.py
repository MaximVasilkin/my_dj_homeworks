from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        list_of_true = []
        for form in self.forms:
            print(form.cleaned_data)
            list_of_true.append(form.cleaned_data.get('is_main', None))
        if list_of_true.count(True) > 1 or list_of_true.count(True) < 1:
            raise ValidationError('Главный тег может быть только один')
        return super().clean()

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

class ScopeInLine(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInLine]
    list_display = ['title']
