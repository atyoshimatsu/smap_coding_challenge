from . import views
from django.urls import path

urlpatterns = [
    path('', views.summary, name='summary'),
    path('summary/', views.summary, name='summary'),
    path('detail/', views.detail, name='detail'),
    path('user_detail/<str:pk>', views.user_detail, name='user_detail'),#detail画面からユーザIDをpｋとして受け取る
]
