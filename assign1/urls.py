from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect




urlpatterns = [
    # so the root will direct directly to the shop app
    url(r'^$', lambda r: HttpResponseRedirect('shop/')),
    url(r'^admin/', admin.site.urls),
    url(r'^shop/', include('shop.urls')),
]

# Whenever we are in dev mode, use the following settings for uploading of files/ images
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
