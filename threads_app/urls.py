from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_site, name='login_site'),
    path('logout/', views.logout_site, name='logout_site'),
    path('posts/', views.posts, name='posts'),
    path('posts/<str:code>/', views.post_detail, name='post_detail_url'),
    path('create_post/', views.create_post, name = 'create_post'),
    path('edit_post/<str:code>/', views.edit_post, name = 'edit_post'),
    path('delete_post/<str:code>/', views.post_delete, name = 'post_delete'),
    path('profile/<str:user_id>/', views.profile, name='profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('post_detail/<str:code>/comment/', views.comment, name='comment'),
    path('search/', views.search, name='search'),
    path('posts/<str:code>/like/', views.like, name = 'like'),
    # path('send_message/<int:sender_id>/<int:receiver_id>/', send_message, name='send_message'),
    # path('message/<int:sender_id>/<int:receiver_id>/', message, name='message'),
    # path('favourite/<int:user_id>/', favourite, name='favourite'),
    # path('delete_favourite/<int:favourite_id>/', delete_favourite, name='delete_favourite'),
    # path('follow/<int:follower_id>/<int:following_id>/', follow, name='follow'),
    # path('cancel_follow/<int:follow_id>/', cancel_follow, name='cancel_follow'),
]