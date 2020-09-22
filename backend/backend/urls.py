from django.contrib import admin
from django.urls import path
from chat.views import login, logout, list_chatrooms

urlpatterns = [
    path('login/', login),
    path('logout/', logout),

    path('chatlist/<int:chatroom_id>/', list_chatrooms),
    path('admin/', admin.site.urls),
]
