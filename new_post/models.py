from django.db import models
from django.contrib.auth.models import User

# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=128)
#     body = models.CharField(max_length=400)


# def get_image_filename(instance, filename):
#     title = instance.post.title
#     slug = slugify(title)
#     return "post_images/%s-%s" % (slug, filename)


# class Images(models.Model):
#     post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=get_image_filename,
#                               verbose_name='Image')