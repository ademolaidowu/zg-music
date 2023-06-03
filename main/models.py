from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class University(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name





OPTIONS = (
    (1,"Horizontal - 728x90"),
    (2,"Vertical - 300x600"),
    (3,"Video - 720x405"),
    (4,"Youtube video - 720x405")
)

class Advertisement(models.Model):
    title       = models.CharField(max_length=150)
    owner       = models.CharField(max_length=150)
    type        = models.IntegerField(choices=OPTIONS, default=1)
    image       = models.ImageField(upload_to='advertisement', blank=True, null=True, help_text='Optional')
    video       = models.FileField(upload_to='advertisement', blank=True, null=True, help_text='Optional')
    youtube     = models.CharField(max_length=150, blank=True, null=True, help_text='Optional')
    description = models.TextField(blank=True, null=True, help_text='Required only for videos and youtube ads')
    link        = models.URLField(max_length=200, help_text='Required only for youtube video ads', blank=True, null=True)
    active      = models.BooleanField(default=True)
    posted      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return self.title





class Video(models.Model):
    title       = models.CharField(max_length=200)
    feature     = models.TextField(max_length=225, null=True, blank=True)
    artist      = TaggableManager()
    description = models.TextField(max_length=225, null=True, blank=True, help_text='Optional')
    university  = models.ManyToManyField('University', blank=True, related_name='institutions')
    link        = models.CharField(max_length=225, verbose_name='Youtube Link')
    active      = models.BooleanField(default=True)
    created     = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} by {self.feature}'




class Audio(models.Model):
    title       = models.CharField(max_length=200)
    file        = models.FileField(upload_to='audio')
    type        = models.CharField(max_length=200)
    active      = models.BooleanField(default=True)
    date        = models.DateTimeField(default=timezone.now)





class CustomerService(models.Model):
    name    = models.CharField(max_length=200)
    email   = models.EmailField(max_length=200)
    phone   = models.IntegerField(blank=True, null=True, verbose_name='Phone Number')
    content = models.TextField(verbose_name='Message')
    date    = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Customer Service'

    def __str__(self):
        return self.name




