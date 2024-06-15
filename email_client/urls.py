from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('inbox', views.InMailBox.as_view(), name='inbox'),
    path('send', views.SendMessageView.as_view(), name='send_message'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),


]