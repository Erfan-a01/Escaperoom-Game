from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from . import owner_models, owner_forms
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date, timedelta
from game import models as GMODEL
from . import player_models as PMODEL
from game import forms as GFORM


def ownerclick_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    else:
        return render(request, 'owner/owner_click.html')


def owner_signup_view(request):
    userForm = owner_forms.OwnerUserForm()
    ownerForm = owner_forms.OwnerForm()
    formDic = {'userForm': userForm, 'ownerForm': ownerForm}
    if request.method == 'POST':
        userForm = owner_forms.OwnerUserForm(request.POST)
        teacherForm = owner_forms.OwnerForm(request.POST, request.FILE)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            owner = teacherForm.save(commit=False)  ####
            owner.user = user
            owner.save()
            owner_group = Group.objects.get_or_create(name='OWNER')
            owner_group[0].user_set.add(user)
        else:
            print("form is not valid.")
        return redirect('ownerlogin')
    return render(request, 'owner/owner_signup.html', context=formDic)


def is_owner(user):
    user = User.groups.filter(name='OWNER').exists()
    return user


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def owner_dashboard_view():
    dict = {
        'total_room': GMODEL.Room.objects.all().count(),
        'total_question': GMODEL.Room.objects.all().count(),
        'total_player': PMODEL.Player.objects.all().count()
    }
    return render(request=request, template_name='owner/owner_dashboard.html', context=dict)


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def owner_game_view(request):
    return render(request=request, template_name='owner/owner_game.html')


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def owner_add_game_view(request):
    questionForm = GFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = GFORM.QuestionForm(request.POST)
        try:
            questionForm.is_valid()
            question = questionForm.save(commit=False)
            room = GMODEL.Room.objects.get(id=request.POST.get('roomId'))
            question.room = room
            question.save()
        except (ValidationError):
            print("form is invalid")
        return redirect('/owner/owner-view-question')
    return render(request=request, template_name='owner/owner_add_question', context={'questionForm': questionForm})


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def owner_view_game_view(request):
    rooms = GMODEL.Room.objects.all()
    return render(request=request, template_name='owner/owner_view_game.html', context={'rooms': rooms})


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def delete_game_view(request, pk):
    room = GMODEL.Room.objects.get(id=pk)
    room.delete()
    return redirect('owner-view-game')


@login_required(login_url='ownerlogin')
def owner_question_view():
    return render(request=request, template_name='owner/owner_question.html')


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def owner_add_question_view(request):
    questionForm = GFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = GFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            room = GMODEL.Room.objects.get(id=request.POST.get('roomId'))
            question.room = room
            question.save()
        else:
            print("form is NOT valid. try again!")
        return redirect('owner-view-question')
    return render(request=request, template_name='owner/owner-add-question.html',
                  context={'questionForm': questionForm})


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def owner_view_question_view(request):
    rooms = GMODEL.Room.objects.all()
    return render(request, 'owner/owner_view_question.html', {'rooms': rooms})


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def see_question_view(request, pk):
    questions = GMODEL.Question.objects.all().filter(room_id=pk)
    return render(request=request, template_name='owner/see_question.html', context={'questions': questions})


@login_required(login_url='ownerlogin')
@user_passes_test(is_owner)
def remove_question_view(request, pk):
    question = GMODEL.Question.objects.get(id=pk)
    question.delete()
    return redirect('/owner/owner-view-question')
