from django.shortcuts import render
from django.views import generic
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

class PostList(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    queryset = Post.objects.filter(status__gte=0).order_by('-created_on')
    context_object_name = 'post_list'
    template_name = 'index.html'

    def post(self, request, **kwargs):
        post_data = request.POST
        start_date = post_data['startDate']
        end_date = post_data['endDate']
        self.queryset = Post.objects.filter(status__gte=0, created_on__range=[start_date, end_date]).order_by('-created_on')
        context = {'post_list': self.queryset}
        return render(request, self.template_name, context)



class PostDetail(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = 'post_detail.html'

    def post(self, request, **kwargs):
        current_url = request.build_absolute_uri()
        split_url = current_url.split('/')
        if current_url.endswith('/'):
            slug = split_url[-2]
        else:
            slug = split_url[-1]
        current_post = Post.objects.get(slug=slug)

        post_data = request.POST
        action = post_data['privacyToggle']
        if action == 'makePrivate':
            current_post.status = 1
            current_post.save()
        elif action == 'makePublic':
            current_post.status = 0
            current_post.save()
        return render(request, self.template_name, {'post': current_post})



class PublicPostList(generic.ListView):
    paginate_by = 10
    redirect_field_name = 'redirect_to'
    queryset = Post.objects.filter(status=0).order_by('-created_on')
    context_object_name = 'post_list'
    template_name = 'index.html'

    def post(self, request, **kwargs):
        post_data = request.POST
        start_date = post_data['startDate']
        end_date = post_data['endDate']
        self.queryset = Post.objects.filter(status=0, created_on__range=[start_date, end_date]).order_by('-created_on')
        context = {'post_list': self.queryset}
        return render(request, self.template_name, context)


class PublicPostDetail(generic.DetailView):
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = 'post_detail.html'

    def post(self, request, **kwargs):
        current_url = request.build_absolute_uri()
        split_url = current_url.split('/')
        if current_url.endswith('/'):
            slug = split_url[-2]
        else:
            slug = split_url[-1]
        current_post = Post.objects.get(slug=slug)

        post_data = request.POST
        action = post_data['privacyToggle']
        if action == 'makePrivate':
            current_post.status = 1
            current_post.save()
        elif action == 'makePublic':
            current_post.status = 0
            current_post.save()
        return render(request, self.template_name, {'post': current_post})


class CustomLogin(generic.View):
    redirect_field_name = 'redirect_to'
    template_name = 'login.html'

    def get(self, request, **kwargs):
        return render(request, 'login.html', {})

# def login(request):
#     return render(request, 'login.html', '')