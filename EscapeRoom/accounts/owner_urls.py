from django.urls import path
from . import owner_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # ********************* Owner main paths ********************************************************
    path('ownerclick', owner_views.ownerclick_view),
    path('ownerlogin', LoginView.as_view(template_name='owner/owner_login.html'), name='ownerlogin'),
    path('ownersignup', owner_views.owner_signup_view, name='ownersignup'),
    path('owner-dashboard', owner_views.owner_dashboard_view, name='owner-dashboard'),
    path('owner-game', owner_views.owner_game_view, name='owner-game'),
    path('owner-add-game', owner_views.owner_add_game_view, name='owner-add-game'),
    path('owner-view-game', owner_views.owner_view_game_view, name='owner-view-game'),
    path('delete-game/<int:pk>', owner_views.delete_game_view, name='delete-game'),
    # ***************************** Question paths ********************************************************
    path('owner-question', owner_views.owner_question_view, name='owner-question'),
    path('owner-add-question', owner_views.owner_add_question_view, name='owner-add-question'),
    path('owner-view-question', owner_views.owner_view_question_view, name='owner-view-question'),
    path('see-question/<int:pk>', owner_views.see_question_view, name='see-question'),
    path('remove-question/<int:pk>', owner_views.remove_question_view, name='remove-question'),
]
