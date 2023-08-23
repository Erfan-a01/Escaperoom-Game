"""
URL configuration for EscapeRoom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from game import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [

    path('owner/', admin.site.urls),
    path('owner/', include('accounts.owner_urls')),
    path('player/', include('accounts.player_urls')),
    # **************************** account paths ***********************************************
    path('', views.home_view, name=''),
    path('logout/', LogoutView.as_view(template_name='player/logout.html'), name='logout'),
    path('contactus', views.contact_us_view),
    path('afterlogin', views.after_login_view, name='afterlogin'),
    # ***************************** owner-owner paths ****************************************************
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='game/adminlogin.html'), name='adminlogin'),
    path('owner-dashboard', views.admin_dashboard_view, name='owner-dashboard'),
    path('owner-owner', views.admin_owner_view, name='owner-owner'),
    path('owner-view-owner', views.admin_view_owner_view, name='owner-view-owner'),
    path('update-owner/<int:pk>', views.update_owner_view, name='update-owner'),
    path('delete-owner/<int:pk>', views.delete_owner_view, name='delete-owner'),
    path('owner-view-pending-owner', views.admin_view_pending_owner_view, name='owner-view-pending-owner'),
    # path('owner-view-owner-salary', views.admin_view_teacher_salary_view, name='owner-view-owner-salary'),
    path('approve-owner/<int:pk>', views.approve_owner_view, name='approve-owner'),
    path('reject-owner/<int:pk>', views.reject_owner_view, name='reject-owner'),
    # ***************************** owner-player paths ******************************************************
    path('owner-player', views.admin_player_view, name='owner-player'),
    path('owner-view-player', views.admin_view_player_view, name='owner-view-player'),
    path('owner-view-player-score', views.admin_view_player_score_view, name='owner-view-player-score'),
    path('owner-view-score/<int:pk>', views.admin_view_score_view, name='owner-view-score'),
    path('owner-check-score/<int:pk>', views.admin_check_score_view, name='owner-check-score'),
    path('update-player/<int:pk>', views.update_player_view, name='update-player'),
    path('delete-player/<int:pk>', views.delete_player_view, name='delete-player'),
    # ****************************** owner-room paths ****************************************************
    path('owner-room', views.admin_room_view, name='owner-room'),
    path('owner-add-room', views.admin_add_room_view, name='owner-add-room'),
    path('owner-view-room', views.admin_view_room_view, name='owner-view-room'),
    path('delete-room/<int:pk>', views.delete_room_view, name='delete-room'),
    # ******************************* owner-question paths ****************************************************
    path('owner-question', views.admin_question_view, name='owner-question'),
    path('owner-add-question', views.admin_add_question_view, name='owner-add-question'),
    path('owner-view-question', views.admin_view_question_view, name='owner-view-question'),
    path('view-question/<int:pk>', views.view_question_view, name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view, name='delete-question'),

]
