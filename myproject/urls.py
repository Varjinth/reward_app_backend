"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from logs.views import *  





urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('check-auth/', check_authentication, name='trip-approve'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("apps/", AppListCreateAPIView.as_view(), name="app-list-create"),  #get.,post, delete
    path("apps/<int:pk>/", AppListCreateAPIView.as_view(), name="app-list-create"),  #delete
    path("tasks/", UserTaskCreateAPIView.as_view(), name="task-list-create"), #post
    path('tasks/completed/', CompletedTasksView.as_view(), name='completed-tasks'), #get
    path('tasks/pending/', PendingTasksView.as_view(), name='pending-tasks'), #get
    path("user/details/", UserDetailsView.as_view(), name="user-details"), #get
]

