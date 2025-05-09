from django.shortcuts import render, redirect, reverse
from account.forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("main"))
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse("main"))
            else:
                form.add_error(None, "사용자 정보가 일치하지 않습니다. 다시 입력해주세요.")
        return render(request, "account/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(reverse("main"))
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logout_view(request) # 로그인이 로그아웃 되게 실행
            return redirect(reverse("account:login")) # logout_view를 안넣으면 회원가입시 로그인이 되어있기에 main으로 넘어가게 연결됌
    else:
        form = SignUpForm()
    return render(request, "account/signup.html", {"form": form})

