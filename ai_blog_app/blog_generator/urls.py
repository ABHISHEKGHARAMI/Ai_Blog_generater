from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('generate-blog/', views.generate_blog, name='generate-blog'),
    path('generate-list/',views.user_list_view,name='generate-list'),
    path('generate-detail/<int:pk>/',views.user_blog_detail_view, name='generate-detail'),
]
