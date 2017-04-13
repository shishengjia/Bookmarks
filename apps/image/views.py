from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from utils.LoginJudge import LoginRequiredMixin
from users.forms import LoginForm
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ImageCreatView(View):
    def get(self, request):
        """
        从外部网站通过bookmarklet获取图片后，跳转到这里进行处理
        """
        if not request.user.is_authenticated():
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
        form = ImageCreateForm(data=request.GET)
        return render(request, 'create.html', {
            'section': 'images',
            'form': form
        })

    def post(self, request):
        """
        进行图片的提交
        """
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_item.get_absolute_url())
        return render(request, 'create.html', {
                'section': 'images',
                'form': form
            })


class ImageDetailView(View):
    """
    图片详情页
    """
    def get(self, request, id):
        image = get_object_or_404(Image, id=id)
        # has_fav = False
        # users = image.users_like.all()
        # if request.user in users:
        #     has_fav = True
        return render(request,
                      'detail.html',
                      {'section': 'images',
                       'image': image})


class ImageLikeView(View, LoginRequiredMixin):
    def post(self, request):
        if not request.user.is_authenticated():
            form = LoginForm()
            return JsonResponse({'status': 'not login'})
        image_id = request.POST.get('id')
        action = request.POST.get('action')
        if image_id and action:
            try:
                image = Image.objects.get(id=image_id)
                if action == 'like':
                    image.users_like.add(request.user)
                    return JsonResponse({'status': 'ok'})
                else:
                    image.users_like.remove(request.user)
                    return JsonResponse({'status': 'ok'})
            except:
                pass
        return JsonResponse({'status': 'ko'})


class ImageListView(View):
    def get(self, request):
        images = Image.objects.all()
        paginator = Paginator(images, 8)
        page = request.GET.get('page')
        try:
            images = paginator.page(page)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            images = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, '', {'section': 'images',
                                        'images': images})
        return render(request, '', {'section': 'images',
                                    'images': images})
