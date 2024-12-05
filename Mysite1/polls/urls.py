from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.home, name='basic'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile-edit'),
    path('delete/', views.delete_profile, name='delete_profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create/', views.create_question, name='create_question'),


]