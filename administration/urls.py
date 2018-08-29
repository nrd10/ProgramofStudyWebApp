from django.urls import path, include
from django.conf.urls import url
from django_filters.views import FilterView
from administration import views

urlpatterns = [
    path('search/', views.searchoptions, name='admin-search'),
    path('create/', views.admincreate, name='admin-create'),
    path('updatedb/', views.updatedb, name='admin-update'),
    path('populatedb/', views.populatedb, name='admin-populate-database'),
    path('coursedelete/', views.fullcoursedelete, name='admin-fullcourse-delete'),
    path('database/', views.admindatabase, name='admin-database'),
    path('coursesearch/', views.CourseSearch, name='admin-courses'),
    path('course/', views.CourseCreateView.as_view(), name='admin-course-create'),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name='admin-course-detail'),
    path('course/<int:pk>/update', views.CourseUpdateView.as_view(), name='admin-course-update'),
    url(r'^course/(?P<form_id>[0-9]+)/delete$', views.coursedelete, name='admin-course-delete'),
    path('useroptions/', views.usercontrols, name='admin-user-options'),
    path('usersearch/', views.UserSearch, name='admin-user-search'),
    path('createuser/', views.UserCreate.as_view(), name='admin-user-create'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='admin-user-detail'),
    path('user/<int:pk>/update', views.UserUpdateView.as_view(), name='admin-user-update'),
    url(r'^user/(?P<form_id>[0-9]+)/delete$', views.userdelete, name='admin-user-delete'),
    path('studentupload/', views.upload, name='admin-student-upload'),
    path('duke_login/', views.duke_login, name='admin-duke-oauth'),
]
