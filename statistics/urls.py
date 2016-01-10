from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.main, name='main'),
    url(r'^client_detail/(?P<NO>[0-9]+)/$', views.client_detail, name='client_detail'),
]
