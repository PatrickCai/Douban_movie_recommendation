from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from recommendation import views
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^admin/', include(admin.site.urls)),

    #let;s 
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'entrance', views.entrance, name='entrance'),
    # url(r'xiami', xia.views.login, name='xiami'),
    url(r'^result', views.result, name='result'),
    url(r'^create', views.create),
    url(r'^people/(.+)', views.result, name='result')

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.POSTER_URL, document_root=settings.POSTER_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


