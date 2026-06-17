import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import debug_toolbar

from catalog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start_page),
    path('places/<int:place_id>/', views.parse_place_details, name='parse_place_details'),
    path('tinymce/', include('tinymce.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(
        settings.BASE_DIR, 'static'))