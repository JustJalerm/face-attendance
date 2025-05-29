from django.contrib import admin
from django.urls import path, include
from accounts.views import home_redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),  # Redirect root URL to login page
    path('accounts/', include('accounts.urls')),
    path('classroom/', include('classroom.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)