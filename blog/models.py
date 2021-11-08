from django.db import models
from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    display_author = models.CharField(max_length=200, unique=False)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    img_0 = models.ImageField(upload_to='pics', default=0)
    img_1 = models.ImageField(upload_to='pics', default=0)
    img_2 = models.ImageField(upload_to='pics', default=0)
    img_3 = models.ImageField(upload_to='pics', default=0)
    img_4 = models.ImageField(upload_to='pics', default=0)
    img_5 = models.ImageField(upload_to='pics', default=0)
    img_6 = models.ImageField(upload_to='pics', default=0)
    img_7 = models.ImageField(upload_to='pics', default=0)
    img_8 = models.ImageField(upload_to='pics', default=0)
    img_9 = models.ImageField(upload_to='pics', default=0)
    video = models.FileField(upload_to='videos', default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
