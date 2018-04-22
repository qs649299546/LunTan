# coding: utf8

from django.shortcuts import render, redirect

from user.models import User, Permission


def check_perm(need_perm):
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            uid = request.session.get('uid')
            try:
                user = User.objects.get(id=uid)
            except Exception as e:
                return redirect('/')

            if user.has_perm(need_perm):
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'blockers.html')
        return wrap2
    return wrap1
