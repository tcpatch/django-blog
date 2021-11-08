from django.shortcuts import render, HttpResponseRedirect
from django.core.files.base import ContentFile
# from django.contrib import messages
# from django.forms import modelformset_factory
from .forms import NewPost
# from .models import Images
from blog.models import Post
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewPost(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            User = get_user_model()
            users = User.objects.all()
            p = Post()
            p.title = request.POST['title']
            p.slug = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            selected_user = None
            for user in users:
                if user.username == request.POST['author']:
                    selected_user = user
            assert(selected_user is not None)
            p.author = selected_user
            display_author = request.POST['author']
            p.display_author = display_author
            p.content = request.POST['content']
            if request.get_full_path().endswith('new_post/edit/'):
                p.status = 0
            else:
                p.status = request.POST['status']
            # 1 = private
            # 0 = public
            for i, f in enumerate(request.FILES.getlist('image')):
                setattr(p, 'img_{}'.format(i), f)
            if 'video' in form.files:
                p.video = form.files['video']
            #legacy...
            #p.img = form.files['image']
            p.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewPost()
    if request.get_full_path().endswith('new_post/edit/'):
        return render(request, 'new_post/new_post.html', {'form': form})
    else:
        return render(request, 'new_post/index.html', {'form': form})

@login_required
def edit_post(request, slug):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if 'delete_status' in request.POST:
            if request.POST['delete_status'] == 'delete':
                post_to_delete = Post.objects.get(slug=slug)
                post_to_delete.delete()
                return HttpResponseRedirect('/private/')

        # create a form instance and populate it with data from the request:
        form = NewPost(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            User = get_user_model()
            users = User.objects.all()
            p = Post.objects.get(slug=slug)
            p.title = request.POST['title']
            selected_user = None
            for user in users:
                if user.username == request.POST['author']:
                    selected_user = user
            assert(selected_user is not None)
            p.author = selected_user
            p.display_author = request.POST['author'].replace('_', ' ')
            p.content = request.POST['content']
            p.status = request.POST['status']
            # 1 = private
            # 0 = public
            for i, f in enumerate(request.FILES.getlist('image')):
                setattr(p, 'img_{}'.format(i), f)
            if 'video' in form.files:
                p.video = form.files['video']
            #legacy...
            #p.img = form.files['image']
            p.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/private/')

    # if a GET (or any other method) we'll create a blank form
    else:
        current_post = Post.objects.get(slug=slug)
        form = NewPost()
        form.fields['title'].initial = current_post.title
        form.fields['author'].initial = current_post.author
        form.fields['content'].initial = current_post.content

    return render(request, 'new_post/index.html', {'form': form, 'slug': slug})
