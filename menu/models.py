from django.core import validators
from django.db import models
from django.urls import reverse, NoReverseMatch

from .utils import query_debugger


class TreeMenuType(models.Model):

    class Meta:
        verbose_name = 'Menu type'
        verbose_name_plural = 'Menu types'

    name = models.CharField(verbose_name='Name', max_length=100, blank=False, null=False)
    verbose_name = models.CharField(verbose_name='Verbose name', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.verbose_name or self.name


class CustomURLValidator(validators.URLValidator):
    def __call__(self, value):
        try:
            reverse(value)
        except NoReverseMatch:
            super().__call__(value)


class TreeMenuItem(models.Model):

    class Meta:
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'

    name = models.CharField(verbose_name='name', max_length=255, blank=False, null=False)
    menu_type = models.ForeignKey('TreeMenuType', verbose_name='Menu type', on_delete=models.CASCADE, blank=False, null=False)
    parent = models.ForeignKey('self', verbose_name='Parent item', null=True, blank=True, default=None, on_delete=models.CASCADE)
    url = models.CharField(verbose_name='URL', max_length=2048, blank=True, null=False, validators=[CustomURLValidator()])

    def __str__(self):
        parent_str = f'{self.parent} ->' if self.parent else ''
        return f'{parent_str}{self.name}'

    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, models.CharField):
                value = getattr(self, field.name)
                if value:
                    setattr(self, field.name, value.strip())

    @classmethod
    @query_debugger
    def get_menu(cls, name: str):
        return TreeMenuItem.objects.select_related().filter(menu_type__name=name).order_by('pk')



