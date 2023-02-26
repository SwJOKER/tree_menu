from collections import OrderedDict
from django import template
from django.http import HttpRequest
from django.template import RequestContext
from django.urls import reverse, NoReverseMatch

from ..models import TreeMenuItem

register = template.Library()


@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context: RequestContext, name: str = '', parent: int = None):
    if not name:
        return
    menu = context.get('full_menu')
    if parent and menu:
        active_branch = context.get('active_branch')
    else:
        request = context.get('request')
        # there is could be used common dict,
        # after python 3.6 it does not matter, but I leaved OrderedDict as mark that in this case order is important,
        # because query to db includes 'order_by'
        menu = OrderedDict()
        selected_id = ''
        if isinstance(request, HttpRequest):
            current_url = request.path
        else:
            current_url = ''
        for item in TreeMenuItem.get_menu(name):
            try:
                url = reverse(item.url)
                target = ''
            except NoReverseMatch:
                target = '_blank'
                url = item.url
            menu.update({item.pk: {
                'parent_id': item.parent_id,
                'url': url,
                'name': item.name,
                'selected': url == current_url,
                'target': target
            }})
            if url == current_url:
                selected_id = item.pk
        active_branch = []
        while selected_id:
            active_branch.append(selected_id)
            selected_id = menu[selected_id]['parent_id']
    return {
        'active_branch': active_branch,
        'menu_name': name,
        'full_menu': menu,
        'root': not parent,
        'active': parent in active_branch or not parent,
        'current_menu': {key: item for key, item in menu.items() if item.get('parent_id') == parent},
    }
