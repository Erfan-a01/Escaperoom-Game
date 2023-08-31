from django.urls import path
from django.contrib.auth.views import LoginView
from . import player_views

urlpatterns = [
    # **************************** Player main paths *************************************
    path('playerclick', player_views.playerclick_view),
    path('playerlogin', LoginView.as_view(template_name='player/playerlogin.html'), name='playerlogin'),
    path('playersignup', player_views.player_signup_view, name='playersignup'),
    path('player-dashboard', player_views.player_dashboard_view, name='player-dashboard'),
    path('player-exam', player_views.player_game_view, name='player-game'),
    path('take-game/<int:pk>', player_views.take_game_view, name='take-game'),
    path('start-game/<int:pk>', player_views.start_game_view, name='start-game'),
    # ****************************** Result and scores paths*********************************************************
    path('calculate-score', player_views.calculate_score_view, name='calculate-score'),
    path('view-result', player_views.view_result_view, name='view-result'),
    path('check-score/<int:pk>', player_views.check_score_view, name='check-score'),
    path('player-score', player_views.player_scores_view, name='player-marks'),
]
