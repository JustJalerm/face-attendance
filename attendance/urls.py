from django.contrib import admin
from django.urls import path, include
from accounts.views import home_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),  # Redirect root URL to login page
    path('accounts/', include('accounts.urls')),
]
