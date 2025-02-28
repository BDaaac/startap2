from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm


@login_required
def post_registration_view(request):
    return render(request, 'accounts/post_registration.html', {
        'user': request.user,
        'logo': 'SkillFlowLogo.png'
    })


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = form.cleaned_data.get("username")
            user.email = form.cleaned_data.get("email")
            user.set_password(form.cleaned_data.get("password1"))  # Устанавливаем пароль
            user.save()
            login(request, user)
            return redirect("post_registration")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form, "logo": "SkillFlowLogo.png"})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = form.cleaned_data.get("username")
            user.email = form.cleaned_data.get("email")
            user.set_password(form.cleaned_data.get("password1"))
            user.save()
            login(request, user)
            return redirect("menu")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url if next_url else "menu")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form, "next": next_url})
