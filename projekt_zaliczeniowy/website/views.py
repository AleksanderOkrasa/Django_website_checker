
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test


from .forms import SignUpForm, LoginForm, EditUserForm
from .models import WebpageData, UserData
from .python_only import log, webpage_data, user_web_data, user_add_up, web_add_up



def signup(request):        #rejestracja
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            log.info(f"User {username} just registered")
            return redirect('/website/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):    #wbudowana funkcja login (dlatego login_view)
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                log.info(f"User {username} just logged in")
                return redirect('/website/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):   #wbudowana funkcja logout (dlatego logout_view)
    logout(request)
    log.info(f"User {request.user} just logged out")
    return redirect('/website/login/')

@login_required
def home(request):          #strona główna
    log.info(f"User {request.user} went to the homepage")
    return render(request, 'website/home.html')

def user_list(request):     #lista użytkowników
    users = User.objects.all()
    count = user_add_up()
    log.info(f"User {request.user} went to the user list")
    return render(request, 'user/user_list.html', {'users': users, 'count': count})

def webpage_list(request):  #lista wyszukiwanych stron
    webs = WebpageData.objects.all()
    count = web_add_up()
    log.info(f"User {request.user} went to the webpage list")
    return render(request, 'website/webpage_list.html', {'webs': webs, 'count': count})


@login_required
def webpage_detail(request, name_webpage):
    web = WebpageData.objects.get(pk = name_webpage)
    users = web.users.all()
    log.info(f'displaying data about the website {web} to the user {request.user}')
    return render(request, 'website/webpage_detail.html', {'users': users, 'web': web})

@login_required
def user_detail(request, username):                     #informacje o uzytkowniku wybranym z listy user_list,
    users = UserData.objects.filter(user = username)    #jeśli jestes zalogowany jako admin to masz dodatkowo
    user = User.objects.get(username = username)        #przycisk umożliwiający usunięcie danego użytkownika
    if request.user.is_superuser:
        account = "super"
        log.info(f'{request.user} is a superuser')
    else:
        account = "normal"
        log.info(f'{request.user} is a normal user')

    log.info(f'displaying data about the user {user} to the user {request.user}')

    return render(request, 'user/user_detail.html', {'users': users, 'user': user, 'account': account})

@user_passes_test(lambda u: u.is_superuser)
def delete_superuser(request, username):                #usunięcie użytkownika z poziomu superusera
    users = UserData.objects.filter(user = username)
    user = User.objects.get(username = username)
    if request.method == 'POST':
        user = username
        user.delete()
        log.info(f'Superuser {request.user} deleted user {user}')
        return redirect('/website/users/')
    log.info(f"Superiser {request.user} went to the subpage delete user {user}")
    return render(request, 'registration/delete_superuser.html', {'users': users, 'user': user})

@login_required
def show_profile(request):      #pokazuje profil aktualnie zalogowanego użytkownika
    user = request.user
    log.info(f'displaying data about his profile to {user}')
    return render(request, 'user/profile.html', {'user': user})

@login_required
def edit_user(request):         #pozwala edytować dane aktualnie zalogowanego użytkownika
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/website/profile')
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'user/edit/edit.html', {'form': form})

@login_required
def change_password(request):        #pozwala edytować hasło aktualnie zalogowanego użytkownika
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/website/')
        else:
            return redirect('fail')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/edit/change_password.html', {'form': form})

@login_required
def delete_user(request):           #usunięcie aktualnie zalogowanego użytkownika
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('/website/')
    return render(request, 'registration/delete.html')

@login_required
def search(request):            #wyszukiwanie strony
    if request.method == 'POST':
        input = (request.POST.get('webpage'))
        log.info(f'User {request.user} search "{input}"')

        illegal_starts = ('http://', 'https://', 'www.')
        for start in illegal_starts:
            if input.startswith(start):
                input = input[len(start):]
                log.info(f'the input was ben changed, deleted "{start}"')
        print(input)
        search_value = input
        webpage = input.replace("/", "..")      #modyfikacja inputu, zamiana / na .. żeby można było
        current_user = str(request.user)        #wejść w wynik wyszukiwania strony z podstronami
                                        #(żeby wyszukiwana strona była traktowana jako jedna podstrona mojego programu)
        webpage_data(search_value, webpage, current_user)
        user_web_data(current_user, webpage)

        return redirect(f'/website/search/{webpage}/')

    return render(request, 'website/search.html')


@login_required
def result_of_search_webpage(request, name_webpage):        #wyświetlenie wyników wyszukiwania
    #search_value = name_webpage.replace("..", "/")
    web = WebpageData.objects.get(pk = name_webpage)
    log.info(f'showing data from {name_webpage} for user {request.user}')
    return render (request, 'website/results_of_search_webpage.html', {'web': web, 'user': request.user})



