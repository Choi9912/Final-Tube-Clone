from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST.get("email", "")

        if not (username and password):
            return HttpResponse("이름과 패스워드는 필수입니다!")

        if User.objects.filter(username=username).exists():
            return HttpResponse("이미 존재하는 사용자입니다!")

        if email and User.objects.filter(email=email).exists():
            return HttpResponse("이미 존재하는 이메일입니다!")

        user = User.objects.create_user(username, email, password)
        user.save()

        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("user_profile")
    else:
        return render(request, "accounts/user_signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user_profile")
        else:
            return render(
                request,
                "accounts/user_login.html",
                {"error": "아이디나 패스워드가 틀렸습니다."},
            )
    else:
        return render(request, "accounts/user_login.html")


def user_logout(request):
    logout(request)
    return redirect("user_login")


@login_required
def user_profile(request):
    return render(request, "accounts/user_profile.html", {"user": request.user})
