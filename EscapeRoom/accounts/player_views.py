from django.shortcuts import render, redirect, reverse
from . import player_forms, player_models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from game import models as GMODEL
from . import owner_models as OMODEL
from django.http import request


def is_player(user):
    return user.groups.filter(name='PLAYER').exists()


def playerclick_view(request):
    if request.user.is_authenticated:
        redirect('afterlogin')
    return render(request=request, template_name='player/player_click.html')


def player_signup_view(request):
    userForm = player_forms.PlayerUserForm()
    playerForm = player_forms.PlayerForm()
    localDict = {'userForm': userForm, 'playerForm': playerForm}
    if request.method == 'POST':
        userForm = player_forms.PlayerUserForm(request.POST)
        playerForm = player_forms.PlayerForm(request.POST)
        if userForm.is_valid() and playerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            player = playerForm.save(commit=False)
            player.user = user
            player.save()
            # I don't know why this is needed!!!:
            # playerGroup = Group.objects.get_or_create(name='PLAYER')
            # playerGroup[0].user_set.add(user)
        return redirect('playerlogin')
    return render(request=request, template_name='player/player_signup.html', context=localDict)


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def player_dashboard_view(request):
    localDict = {
        'rooms_num': GMODEL.Room.objects.all().count(),
        'questions_num': GMODEL.Question.objects.all().count(),
    }
    return render(request=request, template_name='player/player_dashboard.html', context=localDict)


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def player_game_view(request):
    rooms = GMODEL.Room.objects.all()
    return render(request=request, template_name='player/player_game.html', context={'rooms': rooms})


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def take_game_view(request, pk):
    room = GMODEL.Room.objects.get(id=pk)
    questions_num = GMODEL.Question.objects.all().filter(room=room).count()
    questions = GMODEL.Question.objects.all().filter(room=room)
    total_score = 0
    for question in questions:
        total_score += question.score
    return render(request=request,
                  template_name='player/player_game.html',
                  context={'room': room, 'total_score': total_score, 'questions_num': questions_num})


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def start_game_view(request, pk):
    room = GMODEL.Room.objects.get(id=pk)
    questions = GMODEL.Question.objects.all().filter(room=room)
    response = render(request=request, template_name='player/start_game.html',
                      context={'room': room, 'questions': questions})
    # why in this scope a cookie is needed? what will happen if I remove this line:
    response.set_cookie('room_id', room.id)
    return response


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def calculate_score_view(request):
    if request.COOKIES.get('room_id') is not None:
        room_id = request.COOKIES.get('room_id')
        room = GMODEL.Room.objects.get(id=room_id)
        total_score = 0
        questions_num = GMODEL.Question.objects.filter(room=room).count()
        questions = GMODEL.Question.objects.filter(room=room)
        for i in range(questions_num):
            # WARNING: IT MAY CAUSE BUGS:
            entered_ans = request.COOKIES.get(str(i+1))
            right_answer = questions[i].answer
            if entered_ans == right_answer:
                total_score += questions[i].score
        player = player_models.Player.objects.get(user_id=request.user.id)
        result = GMODEL.Result(player=player, room=room, score=total_score)
        result.save()
        return redirect('view-result')


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def view_result_view(request):
    rooms = GMODEL.Room.objects.all()
    return render(request=request, template_name='player/view_result.html', context={'rooms': rooms})


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def check_score_view(request, pk):
    desired_room = GMODEL.Room.objects.get(id=pk)
    desired_player = player_models.Player.objects.get(user_id=request.user.id)
    results = GMODEL.Result.objects.all().filter(room=desired_room).filter(player=desired_player)
    return render(request=request, template_name='player/check_scores.html', context={'results': results})


@login_required(login_url='playerlogin')
@user_passes_test(is_player)
def player_scores_view(request):
    rooms = GMODEL.Room.objects.all()
    return render(request=request, template_name='player/player_scores.html', context={'rooms': rooms})
