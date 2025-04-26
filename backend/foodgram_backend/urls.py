from django.contrib import admin
from django.urls import include, path

from api.views import ShortLinkRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
