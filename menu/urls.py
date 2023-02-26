from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# urlpatterns = [

# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#     path('', index, name='index'),
# ] + [path(f'menu/{i}', index, name=f'index{i}') for i in range(0, 20)] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)