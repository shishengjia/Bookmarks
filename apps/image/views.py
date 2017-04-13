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
    """
    图片点赞
    处理用户点赞传过来的ajax请求
    """
    def post(self, request):
        # 是否登陆
        if not request.user.is_authenticated():
            form = LoginForm()
            return JsonResponse({'status': 'not login'})
        # 获取图片ID和用户行为
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
    """
    For AJAX requests, we render the list_ajax.html template. This template
    will only contain the images of the requested page.
    
    For standard requests, we render the list.html template. This template will
    extend the base.html template to display the whole page and will include
    the list_ajax.html template to include the list of images.  
    """
    def get(self, request):
        images = Image.objects.all()
        paginator = Paginator(images, 8)
        page = int(request.GET.get('page', 1))
        try:
            images = paginator.page(page)
        except EmptyPage:
            # If this the case and the request is done via AJAX,
            # we return an empty HttpResponse that will help us stop the AJAX pagination on the client side
            if request.is_ajax():
                return HttpResponse('')
            images = paginator.page(paginator.num_pages)
        # 如果是ajax请求，表示已经在列表页，用户在下拉网页，加载图片并返回
        if request.is_ajax():
            return render(request, 'list_ajax.html', {'section': 'images',
                                                      'images': images})
        # 刚进入列表页，返回初始数据
        return render(request, 'list.html', {'section': 'images',
                                    'images': images})
