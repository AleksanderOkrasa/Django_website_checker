from django.urls import path

from . import views

app_name= 'website'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='register'),
    path('users/', views.user_list, name='user_list'),
    path('users/<str:username>/', views.user_detail, name='user_detail'),
    path('users/<str:username>/delete/', views.delete_superuser, name='delete_superuser'),
    path('webpages/', views.webpage_list, name='webpage_list'),
    path('webpages/<str:name_webpage>/', views.webpage_detail, name='webpage_detail'),
    path('profile/', views.show_profile, name='profile'),
    path('profile/edit/', views.edit_user, name='edit'),
    path('profile/edit/password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_user, name='delete'),
    path('search/', views.search, name='search'),
    path('search/<str:name_webpage>/', views.result_of_search_webpage, name='results'),
]