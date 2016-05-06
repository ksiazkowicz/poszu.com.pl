"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from api import urls as api_urls

from django.conf import settings

from django.contrib.staticfiles import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from gumtree_crawler import urls as gumtree_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^api/', include(api_urls)),
    url("^$", "web.views.home", name="home"),
    url(r'^item/lost', 'web.views.new_lost_form', name="lost_form"),
    url(r'^item/found', 'web.views.new_found_form', name="found_form"),
    url(r'^item/(?P<item_hash>.*)/auth/(?P<auth_hash>.*)/$', 'web.views.admin_item', name="item_admin"),
    url(r'^item/(?P<item_hash>.*)$', 'web.views.show_item', name="item"),
    url(r'^static/(?P<path>.*)$', views.serve),
    url(r'^success/', 'web.views.success', name="success"),
    url(r'^failure/', 'web.views.failure', name="failure"),
]

for crawler in settings.CRAWLERS:
    urlpatterns += [
        url(r'crawlers/'+crawler[1]+r'/', include(crawler[0]+".urls")),
    ]

urlpatterns += staticfiles_urlpatterns()
