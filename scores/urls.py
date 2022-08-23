from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('auth/', views.auth, name='main-auth'),
    path('edit/', views.edit_members, name='main-edit-members'),
   # path('user_page/', views.user_page, name='main-user-page'),
    re_path(r'^user/(?P<user>[-\w]*)/$', views.user_page, name='main-user-page')

]