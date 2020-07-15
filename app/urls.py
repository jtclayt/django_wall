from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('wall/', views.wall, name='wall'),
    path('messages/create', views.create_message, name='create_message'),
    path('messages/<int:message_id>/destroy', views.destroy_message, name='destroy_message'),
    path('comments/create', views.create_comment, name='create_comment'),
    path('comments/<int:comment_id>/destroy', views.destroy_comment, name='destroy_comment'),
    path('logout', views.logout, name='logout')
]
