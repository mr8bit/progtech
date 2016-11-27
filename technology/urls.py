from django.conf.urls import url , include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    password_change,
    password_change_done,
)
urlpatterns = [
    url(r'^$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^main/', views.home, name='main'),
    url(r'^post/$', views.post, name='post'),
    url(r'^messages/$', views.messages, name='messages'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^groups/(?P<id>[-\w]+)/chat$', views.chat, name='chat'),
    url(r'^groups/(?P<id>[-\w]+)$', views.students, name='students'),
    url(r'^groups/(?P<id_group>[-\w]+)/student/(?P<id>[-\w]+)$', views.student, name='student'),
    url(r'^groups/(?P<id_group>[-\w]+)/student/(?P<id_student>[-\w]+)/laboratory/(?P<id>[-\w]+)$',
        views.laboratory, name='laboratory'),
    url(r'^password/change/$', password_change, {
        'template_name': 'student/change_password.html'},
        name='password_change'),
    url(r'^password/change/done/$', password_change_done,
        {'template_name': 'student/change_password_done.html'},
        name='password_change_done'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
