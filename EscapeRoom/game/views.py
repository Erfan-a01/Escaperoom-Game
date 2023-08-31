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
        approved_by_admin = OMODEL.Owner.objects.all().filter(user_id=request.user.id, situation=True)
        if approved_by_admin is not None:
            return redirect('owner/admin_dashboard')
        else:
            return render(request, 'admin/owner_not_approval.html')
    else:
        return redirect('admin-dashboard')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    local_dict = {
        'total_player': PMODEL.Player.objects.all().count(),
        'total_owner': OMODEL.Owner.objects.all().filter(status=True).count(),
        'total_room': models.Room.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
    }
    return render(request, 'game/admin_dashboard.html', context=local_dict)


@login_required(login_url='adminlogin')
def admin_owner_view(request):
    local_dict = {
        'total_owner': OMODEL.Owner.objects.all().filter(status=True).count(),
        'pending_owner': OMODEL.Owner.objects.all().filter(status=False).count(),
        'salary': OMODEL.Owner.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request, 'game/admin_owner.html', context=local_dict)


@login_required(login_url='adminlogin')
def admin_view_owner_view(request):
    owners = OMODEL.Owner.objects.all().filter(status=True)
    return render(request, 'game/admin_view_owner.html', {'owners': owners})


@login_required(login_url='adminlogin')
def update_owner_view(request, pk):
    owner = OMODEL.Owner.objects.get(id=pk)
    user = OMODEL.User.objects.get(id=owner.user_id)
    userForm = OFORM.OwnerUserForm(instance=user)
    ownerForm = OFORM.OwnerForm(request.FILES, instance=owner)
    mydict = {'userForm': userForm, 'ownerForm': ownerForm}
    if request.method == 'POST':
        userForm = OFORM.OwnerUserForm(request.POST, instance=user)
        ownerForm = OFORM.OwnerForm(request.POST, request.FILES, instance=owner)
        if userForm.is_valid() and ownerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            ownerForm.save()
            return redirect('admin-view-owner')
    return render(request, 'game/update_owner.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_owner_view(request, pk):
    owner = OMODEL.Owner.objects.get(id=pk)
    user = User.objects.get(id=owner.user_id)
    user.delete()
    owner.delete()
    return HttpResponseRedirect('/admin-view-owner')


@login_required(login_url='adminlogin')
def admin_view_pending_owner_view(request):
    owners = OMODEL.Owner.objects.all().filter(status=False)
    return render(request, 'game/admin_view_pending_owner.html', {'owners': owners})


# @login_required(login_url='adminlogin')
# def approve_owner_view(request, pk):
#     ownerSalary = forms.OwnerSalaryForm()
#     if request.method == 'POST':
#         ownerSalary = forms.OwnerSalaryForm(request.POST)
#         if ownerSalary.is_valid():
#             owner = TMODEL.Owner.objects.get(id=pk)
#             owner.salary = ownerSalary.cleaned_data['salary']
#             owner.status = True
#             owner.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-view-pending-owner')
#     return render(request, 'game/salary_form.html', {'ownerSalary': ownerSalary})


@login_required(login_url='adminlogin')
def reject_owner_view(request, pk):
    owner = OMODEL.Owner.objects.get(id=pk)
    user = User.objects.get(id=owner.user_id)
    user.delete()
    owner.delete()
    return HttpResponseRedirect('/admin-view-pending-owner')


@login_required(login_url='adminlogin')
def admin_view_owner_salary_view(request):
    owners = OMODEL.Owner.objects.all().filter(status=True)
    return render(request, 'game/admin_view_owner_salary.html', {'owners': owners})


@login_required(login_url='adminlogin')
def admin_player_view(request):
    dict = {
        'total_player': PMODEL.Player.objects.all().count(),
    }
    return render(request, 'game/admin_player.html', context=dict)


@login_required(login_url='adminlogin')
def admin_view_player_view(request):
    players = PMODEL.Player.objects.all()
    return render(request, 'game/admin_view_player.html', {'players': players})


@login_required(login_url='adminlogin')
def update_player_view(request, pk):
    player = PMODEL.Player.objects.get(id=pk)
    user = PMODEL.User.objects.get(id=player.user_id)
    userForm = PFORM.PlayerUserForm(instance=user)
    playerForm = PFORM.PlayerForm(request.FILES, instance=player)
    mydict = {'userForm': userForm, 'playerForm': playerForm}
    if request.method == 'POST':
        userForm = PFORM.PlayerUserForm(request.POST, instance=user)
        playerForm = PFORM.PlayerForm(request.POST, request.FILES, instance=player)
        if userForm.is_valid() and playerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            playerForm.save()
            return redirect('admin-view-player')
    return render(request, 'game/update_player.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_player_view(request, pk):
    player = PMODEL.Player.objects.get(id=pk)
    user = User.objects.get(id=player.user_id)
    user.delete()
    player.delete()
    return HttpResponseRedirect('/admin-view-player')


@login_required(login_url='adminlogin')
def admin_room_view(request):
    return render(request, 'game/admin_room.html')


@login_required(login_url='adminlogin')
def admin_add_room_view(request):
    roomForm = forms.RoomForm()
    if request.method == 'POST':
        roomForm = forms.RoomForm(request.POST)
        if roomForm.is_valid():
            roomForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-room')
    return render(request, 'game/admin_add_room.html', {'roomForm': roomForm})


@login_required(login_url='adminlogin')
def admin_view_room_view(request):
    rooms = models.Room.objects.all()
    return render(request, 'game/Room.html', {'rooms': rooms})


@login_required(login_url='adminlogin')
def delete_room_view(request, pk):
    room = models.Room.objects.get(id=pk)
    room.delete()
    return HttpResponseRedirect('/admin-view-room')


@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request, 'game/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm = forms.QuestionForm()
    if request.method == 'POST':
        questionForm = forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            room = models.Room.objects.get(id=request.POST.get('roomID'))
            question.room = room
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request, 'game/admin_add_question.html', {'questionForm': questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    rooms = models.Room.objects.all()
    return render(request, 'game/admin_view_question.html', {'rooms': rooms})


@login_required(login_url='adminlogin')
def view_question_view(request, pk):
    questions = models.Question.objects.all().filter(room_id=pk)
    return render(request, 'game/view_question.html', {'questions': questions})


@login_required(login_url='adminlogin')
def delete_question_view(request, pk):
    question = models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')


@login_required(login_url='adminlogin')
def admin_view_player_scores_view(request):
    players = PMODEL.Player.objects.all()
    return render(request, 'game/admin_view_player_scores.html', {'players': players})


@login_required(login_url='adminlogin')
def admin_view_scores_view(request, pk):
    rooms = models.Room.objects.all()
    response = render(request, 'game/admin_view_scores.html', {'rooms': rooms})
    response.set_cookie('player_id', str(pk))
    return response


@login_required(login_url='adminlogin')
def admin_check_scores_view(request, pk):
    room = models.Room.objects.get(id=pk)
    player_id = request.COOKIES.get('player_id')
    player = PMODEL.Player.objects.get(id=player_id)

    results = models.Result.objects.all().filter(game=room).filter(player=player)
    return render(request, 'game/admin_check_scores.html', {'results': results})


def aboutus_view(request):
    return render(request, 'game/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'game/contactussuccess.html')
    return render(request, 'game/contactus.html', {'form': sub})
