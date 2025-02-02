from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='index'),
    path('signup/',views.signup,name='index'),
    path('logout/', views.logout, name='index'),
]
