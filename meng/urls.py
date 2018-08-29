from django.urls import path, include
from django.conf.urls import url
from django_filters.views import FilterView
from meng import views
from meng.filters import *
urlpatterns = [
    #Search URLs
    # url(r'^search/$', views.MengPOSsearch, name='dgs-meng-search'),

    path('advisor/',views.MengAdvisorListView.as_view(), name='advisor-meng'),
    path('advisor/<int:pk>', views.MengAdvisorDetailView.as_view(), name='advisor-meng-detail'),
    path('advisor/history/', views.MengAdvisorHistoryView.as_view(), name='advisor-meng-history'),
    url(r'^advisor/advisorapprove/(?P<form_id>[0-9]+)/$', views.mengadvisorapprove, name='advisor-meng-approve'),
    url(r'^advisor/advisorreject/(?P<form_id>[0-9]+)/$', views.mengadvisorcomment, name='advisor-meng-reject'),
    path('dgs/',views.MengDGSListView.as_view(), name='dgs-meng'),
    # path('dgs/history/',views.MengDGSHistoryView.as_view(), name='dgs-meng-history'),
    path('dgs/history/',views.MengPOSsearch, name='dgs-meng-history'),
    path('dgs/<int:pk>', views.MengDGSDetailView.as_view(), name='dgs-meng-detail'),
    url(r'^dgs/dgsapprove/(?P<form_id>[0-9]+)/$', views.mengdgsapprove, name='dgs-meng-approve'),
    url(r'^dgs/dgsreject/(?P<form_id>[0-9]+)/$', views.mengdgscomment, name='dgs-meng-reject'),
    path('list/', views.MengListView.as_view(), name='meng'),
    path('list/<int:pk>', views.MengDetailView.as_view(), name='meng-detail'),
    path('list/<int:pk>/update', views.MengUpdateView.as_view(), name='meng-detail-update'),
    path('create/', views.MengPOSCreate.as_view(), name='meng-create'),
    path('admin/<int:pk>', views.AdminMengDetailView.as_view(), name='admin-meng-detail'),
    url(r'^admin/(?P<form_id>[0-9]+)/delete$', views.mengdelete, name='admin-meng-delete'),
    path('admin/create', views.AdminMengPOSCreate.as_view(), name='admin-meng-create'),
    path('admin/history/', views.AdminMengPOSsearch, name='admin-meng-history'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
]
