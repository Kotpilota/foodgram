from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        's/<int:recipe_id>/',
        RedirectView.as_view(pattern_name='recipe-detail')
    ),
]
