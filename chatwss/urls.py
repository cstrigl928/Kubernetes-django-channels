
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name="chatwss-page"),    # Core is defined from here we will use polls as alias for 'Core'...
<<<<<<< HEAD
    path('<str:room_name>/', views.room, name="room"),

=======
    path('<str:room_name>/', views.room, name='chat-room'),
    # path('')
>>>>>>> origin/remote-staging
]