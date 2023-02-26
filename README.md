App with realisation tree menu on django and css.
Task terms: 

1) Menu must be developed through tamplate tags.
2) All levels over current menu item must be unwrapped. Level under it must be unwraped too.
3) Menu stored in DB
4) Could be edit in Django Admin
5) Active menu item determine via current url 
6) On the same page could be multiple different menues
7) On click on menu item there is redirection to defined in menu item url. 
Url may be defined by direct link or by named django's url. 
8) For one rendering is one db query

Application must provide posibility to insert menu in db through admin's interface and render it on any page by menu caption like:

{% draw_menu 'main_menu' %}

Task limits:
Using default python libraries and Django only.

The task was completed according to all requirements.

