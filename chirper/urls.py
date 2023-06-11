from django.urls import path
from . import views


app_name = 'chirper'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profile/<str:poster>/', views.profile, name='profile'),
    path('reply/<int:post_id>/', views.reply, name='reply'),
]
