from django.forms import ModelForm, BaseInlineFormSet
from django.urls import reverse
from django.utils.html import format_html_join
from django.contrib import admin
from .models import TreeMenuType, TreeMenuItem


class MenuItemsFormSet(BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs


class MenuItemForm(ModelForm):
    class Meta:
        model = TreeMenuItem
        fields = '__all__'

    def get_parents_avoid_recursive(self, obj):

        def get_branch(item):
            store = [item.id]
            for i in item.treemenuitem_set.all():
                store.extend(get_branch(i))
            return store

        exclude = get_branch(obj)
        return TreeMenuItem.objects.select_related('parent').exclude(pk__in=exclude)


    def __init__(self, *args, **kwargs):
        parent_object = kwargs.pop('parent_object', None)
        super().__init__(*args, **kwargs)
        if self.fields.get('parent'):
            queryset = self.fields['parent'].queryset
            if self.instance.id:
                queryset = self.get_parents_avoid_recursive(self.instance).filter(menu_type=self.instance.menu_type)
            else:
                match parent_object:
                    case TreeMenuItem(), hasattr(parent_object, 'menu_type'):
                        queryset = queryset.filter(menu_type=parent_object.menu_type)
                    case TreeMenuType():
                        queryset = queryset.filter(menu_type=parent_object)
            self.fields['parent'].queryset = queryset

    def save(self, commit=True):

        def get_branch(item):
            store = [item]
            for i in item.treemenuitem_set.all():
                if i:
                    store.extend(get_branch(i))
            return store

        if self.instance.parent:
            if self.instance.id and self.instance.parent.menu_type != self.instance.menu_type:
                self.instance.parent = None
            else:
                self.instance.menu_type = self.instance.parent.menu_type
        self.instance = super().save(commit)
        for item in get_branch(self.instance):
            item.menu_type = self.instance.menu_type
            item.save()
        return self.instance


class TreeMenuItemInline(admin.TabularInline):
    extra = 1
    model = TreeMenuItem
    fields = ('name', 'submenus', 'parent', 'url')
    readonly_fields = ('submenus',)
    form = MenuItemForm
    formset = MenuItemsFormSet
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('parent')

    def submenus(self, obj=None, *args, **kwargs):
        obj = obj.treemenuitem_set.all()
        return format_html_join(
            '',
            '<a href="{}">{}</a><br>',
            ((
                reverse('admin:menu_treemenuitem_change', args=(c.id,)),
                c.name
            ) for c in obj),
        )


class TreeMenuItemRootInline(TreeMenuItemInline):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent=None)




