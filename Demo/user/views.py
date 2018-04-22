from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from user.models import User, Role
from user.forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # 创建 User 对象，并修改密码
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()

            # 分配默认权限
            Role.add_perm(user.id, 'user')

            # 写入 session 数据
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(nickname=nickname)
            if check_password(password, user.password):
                # 写入 session 数据
                request.session['uid'] = user.id
                request.session['nickname'] = user.nickname
                return redirect('/user/info/')
            else:
                return render(request, 'login.html', {'error': '账号密码错误'})
        except User.DoesNotExist as e:
            return render(request, 'login.html', {'error': '账号密码错误'})

    return render(request, 'login.html', {})


def user_info(request):
    uid = request.session.get('uid')
    if uid:
        user = User.objects.get(id=uid)
        return render(request, 'user_info.html', {'user': user})
    else:
        return render(request, 'login.html', {})


def logout(request):
    request.session.flush()
    return redirect('/')
