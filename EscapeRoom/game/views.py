from django.shortcuts import render, redirect, reverse
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User


# Create your views here.


def home_view(request):
    if request.user.is_authenticated:
        return redirect('after-login')
    return render(request, 'game/main.html')


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_player(user):
    return user.groups.filter(name='PLAYER').exists()


