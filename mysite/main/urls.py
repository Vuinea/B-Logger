from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.view_posts, name='view_posts'),
    path('create/', views.create_post, name='create_post'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search', views.search_posts, name='search_posts'),
    path('<int:post_id>/', views.view_post, name='view_post'),
    path('rate_post/<int:post_id>', views.rate_post, name='rate_post'),
    path('manage_favorite/<int:post_id>/', views.manage_favorite, name='manage_favorite'),
]

