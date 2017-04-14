from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm
from .models import UserProfile, Contact


class LoginView(View):
    """
    登陆
    """
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！",
                                                      'form': form})
        else:
            return render(request, 'login.html', {'form': form})


class RegisterView(View):
    """
    注册
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
        return render(request, 'register.html', {'form': form})


class LogoutView(View):
    """
    登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class DashBoardView(View):
    def get(self, request):
        return render(request, 'dashboard.html', {
            'section': 'dashboard'
        })


class UserListView(View):
    """
    用户列表
    """
    def get(self, request):
        users = UserProfile.objects.filter(is_active=True)
        return render(request, 'user_list.html', {'users': users,
                                                  'section': 'people'})


class UserDetailView(View):
    """
    用户详情
    """
    def get(self, request, username):
        user = get_object_or_404(UserProfile, username=username, is_active=True)
        followers = [contact.user_from for contact in Contact.objects.filter(user_to=user)]
        return render(request, 'user_detail.html', {'user': user,
                                                    'section': 'people',
                                                    'followers': followers})


class UserFollowView(View):
    """
    用户关注/取关
    """
    def post(self, request):
        # 是否登陆
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'not login'})

        # 用户ID和用户行为
        user_id = int(request.POST.get('id', ''))
        action = request.POST.get('action', '')
        if user_id and action:
            try:
                user = UserProfile.objects.get(id=user_id)
                if action == 'follow':
                    # 关注用户
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                else:
                    # 取消关注
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({'status': 'ok'})
            except UserProfile.DoesNotExist:
                return JsonResponse({'status': 'ko'})

        return JsonResponse({'status': 'ko'})


