from django.urls import path, include,re_path
from . import  views
#from .views import ListView #ListViewFull

from django.urls import path
from .views import ProgramListView, ProgramDetailView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
   path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
 #   path('register/', views.register, name='register'),
    path('', views.all_data, name='index'),
    path('disk/', views.disk, name='disk'),
    path('users_list/', views.users_list, name='users'),
    path('diff/', views.diff, name='diff'),
   # path('monitor/', views.monitor, name='monitor'),
    path('about/', views.about, name='about'),
    #path('auth/', views.auth, name='auth'),
   #path('apidatas/', views.apidatas, name='apidatas'),
    path('programs/', ProgramListView.as_view(), name='program-list-create'),
    path('programs/<int:program_id>/', ProgramDetailView.as_view(), name='program-retrieve-update'),
   # re_path(r"^(?P<api_name>[a-z]+)", ListView, name='members-objects'),
    #re_path(r"^(?P<api_name>[a-z]+)<?P<program_id>[^/]+/$", ListView, name='members-objects'),

   # re_path(r"^(?P<api_name>[a-z]+)", ListViewFull, name='allmembers-objects'),



]