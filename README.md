App with realisation of tree menu on pure python/django and css.

Task terms: 

1) The menu must be developed through a tamplate tags.
2) All levels over the current menu item must be unwrapped. Level under it must be unwraped too.
3) The menu stored in DB
4) Could be edit in Django Admin
5) An active menu item determine via current url 
6) On the same page could be multiple different menus
7) On click on the menu item there is redirection to defined in menu item url. 
   Url may be defined by direct link or by named django's url. 
8) For one rendering is one db query

The application must provide posibility to insert menu in db through admin's interface and render it on any page by menu caption like:

{% draw_menu 'main_menu' %}

The task limits:
Using a default python libraries and Django only.

The task was completed according to all requirements.

There are two models, for menu type and menu items.
To menu item model is connected URL validator. Its check that url could reversed from name or match as outer url.
All spaces cut off from a charfield values in the model's 'clean' function.

For editing a models in admin interface implemented InlineFormset which connect to Admin Models.
There are two Admin Models. One to edit MenuType and included Menu Items. Other to edit a menu item and a straight related child items.
Menu item contains a 'parent' field, this one could be linked to self. 
For avoiding recursive queries implemented custom form. There are possible choises for parents limited.
When parent's 'menu type' change all inheritors's 'menu types' change too. Also user can't define parent from other 'menu type'. 
Also user can't designite item's parent from other 'menu type'. Before that needs to change this item's value.

For convenience added field in formset to show a child items, it contains links to changing them.

For testing the application implemented sintetic urls with name 'index{n}' where n from 0 to 19 and attached test db. 
In addition in utils.py can be found @query_debugger which shows count of queries to db in function







