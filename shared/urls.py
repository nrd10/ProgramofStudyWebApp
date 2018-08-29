from django.urls import path, include
from django.conf.urls import url
from shared import views

urlpatterns = [
    path('', views.index, name='index'),
    path('external_login', views.middle_request, name='login_index'),
    path('oauth_login', views.OIT_login, name='oauth_login'),

]
