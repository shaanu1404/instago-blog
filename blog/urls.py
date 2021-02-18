from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('blogpost.urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name="about-us"),
    path('accounts/', include('accounts.urls')),
    path('reply/', include('replies.urls')),
    path('tags/', include('tags.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
