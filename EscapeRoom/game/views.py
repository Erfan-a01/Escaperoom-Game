from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from accounts import owner_models as OMODEL
from accounts import player_models as PMODEL
from accounts import owner_forms as OFORM
from accounts import player_forms as PFORM
from django.contrib.auth.models import User

from game import forms


def home_view(request):
    if request.user.is_authenticated:
        return redirect('after-login')
    return render(request, 'game/main.html')


# ------------------- identify the type of user: -------------------------------
def is_owner(user):
    return user.groups.filter(name='OWNER').exists()


def is_player(user):
    return user.groups.filter(name='PLAYER').exists()


# ------------------ Redirect to after login page: -------------------------------
def after_login_view(request):
    if is_player(request.user):
        return redirect('player/player-dashboard')
    if is_owner(request.user):
        approved_by_admin = OMODEL.Admin.objects.all().filter(user_id=request.user.id, situation=True)
        if approved_by_admin is not None:
            return redirect('owner/admin_dashboard')
        else:
            return render(request, 'admin/owner_not_approval.html')
    else:
        return redirect('admin-dashboard')


def contact_us_view(request):
    form = forms.ContactusForm()

    return None


def adminclick_view(request):
    return None


def admin_dashboard_view(request):
    return None


def admin_owner_view(request):
    return None


def admin_view_owner_view(request):
    return None


def update_owner_view(request):
    return None


def delete_owner_view(request):
    return None


def admin_view_pending_owner_view(request):
    return None


def approve_owner_view(request):
    return None


def reject_owner_view(request):
    return None


def admin_player_view(request):
    return None


def admin_view_player_view(request):
    return None


def admin_view_player_score_view(request):
    return None


def admin_view_score_view(request):
    return None


def admin_check_score_view(request):
    return None


def update_player_view(request):
    return None


def delete_player_view(request):
    return None


def admin_room_view(request):
    return None


def admin_add_room_view(request):
    return None


def admin_view_room_view(request):
    return None


def delete_room_view(request):
    return None


def admin_question_view(request):
    return None


def admin_add_question_view(request):
    return None


def admin_view_question_view(request):
    return None


def view_question_view(request):
    return None


def delete_question_view(request):
    return None
