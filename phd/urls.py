from django.urls import path, include
from django.conf.urls import url
from phd import views



urlpatterns = [
    #URLs To Pick Between 3 Options
    path('studentview/', views.phdstudentoption, name='phd-student'),
    path('studentcreate/', views.phdstudentoptioncreate, name='phd-student-create'),
    path('advisorview/', views.phdadvisoroption, name='phd-advisor'),
    path('dgsview/', views.phddgsoption, name='phd-dgs'),

    path('bachelor/', views.PHDBSListView.as_view(), name='phdbachelor'),
    path('bachelor/<int:pk>', views.PHDBSDetailView.as_view(), name='phdbachelor-detail'),
    path('bachelor/<int:pk>/update', views.PHDBSUpdateView.as_view(), name='phdbachelor-detail-update'),
    path('bachelor/advisor/',views.PHDBSAdvisorListView.as_view(), name='advisor-phdbachelor'),
    path('bachelor/advisor/<int:pk>', views.PHDBSAdvisorDetailView.as_view(), name='advisor-phdbachelor-detail'),
    path('bachelor/advisor/history/', views.PHDBSAdvisorHistoryView.as_view(), name='advisor-phdbachelor-history'),
    url(r'^bachelor/advisor/advisorapprove/(?P<form_id>[0-9]+)/$', views.phdbacheloradvisorapprove, name='advisor-phdbachelor-approve'),
    url(r'^bachelor/advisor/advisorreject/(?P<form_id>[0-9]+)/$', views.phdbacheloradvisorcomment, name='advisor-phdbachelor-reject'),
    path('bachelor/dgs/',views.PHDBSDGSListView.as_view(), name='dgs-phdbachelor'),
    path('bachelor/dgs/<int:pk>', views.PHDBSDGSDetailView.as_view(), name='dgs-phdbachelor-detail'),
    path('bachelor/dgs/history/',views.PHDBachelorPOSsearch, name='dgs-phdbachelor-history'),
    url(r'^bachelor/dgs/dgsapprove/(?P<form_id>[0-9]+)/$', views.phdbachelordgsapprove, name='dgs-phdbachelor-approve'),
    url(r'^bachelor/dgs/dgsreject/(?P<form_id>[0-9]+)/$', views.phdbachelordgscomment, name='dgs-phdbachelor-reject'),
    path('bachelor/create/', views.PHDBSPOSCreate.as_view(), name='phdbachelor-create'),
    path('bachelor/admin/<int:pk>', views.AdminPHDBSDetailView.as_view(), name='admin-phdbachelor-detail'),
    path('bachelor/admin/create', views.AdminPHDBSPOSCreate.as_view(), name='admin-phdbachelor-create'),
    path('bachelor/admin/history/', views.AdminPHDBSPOSsearch, name='admin-phdbachelor-history'),
    url(r'^bachelor/admin/(?P<form_id>[0-9]+)/delete$', views.phdbsdelete, name='admin-phdbachelor-delete'),

    path('master/', views.PHDMSListView.as_view(), name='phdmaster'),
    path('master/<int:pk>', views.PHDMSDetailView.as_view(), name='phdmaster-detail'),
    path('master/<int:pk>/update', views.PHDMSUpdateView.as_view(), name='phdmaster-detail-update'),
    path('master/advisor/',views.PHDMSAdvisorListView.as_view(), name='advisor-phdmaster'),
    path('master/advisor/<int:pk>', views.PHDMSAdvisorDetailView.as_view(), name='advisor-phdmaster-detail'),
    path('master/advisor/history/', views.PHDMSAdvisorHistoryView.as_view(), name='advisor-phdmaster-history'),
    url(r'^master/advisor/advisorapprove/(?P<form_id>[0-9]+)/$', views.phdmasteradvisorapprove, name='advisor-phdmaster-approve'),
    url(r'^master/advisor/advisorreject/(?P<form_id>[0-9]+)/$', views.phdmasteradvisorcomment, name='advisor-phdmaster-reject'),
    path('master/dgs/',views.PHDMSDGSListView.as_view(), name='dgs-phdmaster'),
    path('master/dgs/<int:pk>', views.PHDMSDGSDetailView.as_view(), name='dgs-phdmaster-detail'),
    path('master/dgs/history/',views.PHDMasterPOSsearch, name='dgs-phdmaster-history'),
    url(r'^master/dgs/dgsapprove/(?P<form_id>[0-9]+)/$', views.phdmasterdgsapprove, name='dgs-phdmaster-approve'),
    url(r'^master/dgs/dgsreject/(?P<form_id>[0-9]+)/$', views.phdmasterdgscomment, name='dgs-phdmaster-reject'),
    path('master/create/', views.PHDMSPOSCreate.as_view(), name='phdmaster-create'),
    path('master/admin/<int:pk>', views.AdminPHDMSDetailView.as_view(), name='admin-phdmaster-detail'),
    path('master/admin/create', views.AdminPHDMSPOSCreate.as_view(), name='admin-phdmaster-create'),
    path('master/admin/history/', views.AdminPHDMSPOSsearch, name='admin-phdmaster-history'),
    url(r'^master/admin/(?P<form_id>[0-9]+)/delete$', views.phdmsdelete, name='admin-phdmaster-delete'),

]
