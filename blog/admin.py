#!/usr/local/bin/python
# coding=utf-8

from django.contrib import admin
from blog.models import Category, Article
from django import forms
from pagedown.widgets import AdminPagedownWidget

class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', )
    search_fields = ('title', )
    fieldsets = (
        (
            None, 
            {
                'fields': ('title', 'slug')
            }
        ),
    )

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        widgets = {
            'content_markdown' : AdminPagedownWidget(),
        }
        exclude = ['content_markup',]

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    # prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date_publish', 'is_approved')
    search_fields = ('title', 'content_markdown',)
    list_filter = ('categories',)
    fieldsets = (
        (
            None, 
            {
                'fields': ('title', 'slug', 'cover', 'author', 'excerpt', 'content_markdown', 'categories', 'date_publish', 'is_public', 'is_approved', )
            }
        ),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
