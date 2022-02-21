from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, re_path
from django.urls import include, path
from django.views.static import serve

from main.views import *
from mysite import settings

urlpatterns = [
    path('', mainHandler),
    path('login/', loginHandler),
    path('logout', logoutHandler),
    path('register', registerHandler),
    path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    })
]
