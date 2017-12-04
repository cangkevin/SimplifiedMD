from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/simplify/$', views.simplify_text, name='simplify_text'),
]
