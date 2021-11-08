from django.db import models


class Poop(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time']


class Nap(models.Model):
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    class Meta:
        ordering = ['-startTime']


class Feed(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

class Food(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    food_name = models.CharField(max_length=500)

    class Meta:
        ordering = ['-time']
