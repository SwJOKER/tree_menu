from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .forms import MenuItemForm, TreeMenuItemRootInline, TreeMenuItemInline
from .models import TreeMenuType, TreeMenuItem


@admin.register(TreeMenuType)
class TreeMenuTypeAdmin(ModelAdmin):
    fields = ['name', 'verbose_name']
    inlines = [TreeMenuItemRootInline]


def custom_named_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


@admin.register(TreeMenuItem)
class TreeMenuItemAdmin(admin.ModelAdmin):
    fields = ['name', 'menu_type', 'parent', 'url']
    list_display = ('name', 'menu_type', 'parent', 'url')
    form = MenuItemForm
    inlines = [TreeMenuItemInline]
    list_filter = (('parent', admin.EmptyFieldListFilter), ('menu_type__verbose_name', custom_named_filter('Menu Type')))


