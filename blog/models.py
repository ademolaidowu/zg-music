from django.db import models
from django.urls import reverse

from account.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

import sys
from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



STATUS = (
    (0,"Draft"),
    (1,"Published"),
    (2,"Withdrawn")
)


class Author(models.Model):
    name        = models.CharField(max_length=150)
    university  = models.ForeignKey("main.University", on_delete=models.DO_NOTHING, null=True, blank=True)
    image       = models.ImageField(upload_to='author', default='author/default.jpg')
    slug        = models.SlugField(max_length=200, unique=True)


    def save(self, *args, **kwargs):
        try:
            saved_author = Author.objects.get(id=self.id)

            if saved_author.image != self.image:
                img = Img.open(self.image)
                output = BytesIO()
                new_image = img.resize((200, 200))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.slug.split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        except Author.DoesNotExist:
            if self.image == 'author/default.jpg':
                pass

            else:
                img = Img.open(self.image)
                output = BytesIO()
                new_image = img.resize((200, 200))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.slug.split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        super(Author, self).save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse("blog:author-detail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.name





class Blog(models.Model):
    title       = models.CharField(max_length=200, unique=True)
    author      = models.ForeignKey(Author, on_delete=models.CASCADE, default='ZeroGravity')
    content     = RichTextUploadingField(blank=True, null=True)
    image       = models.ImageField(upload_to='blog', default='blog/default.jpg', blank=True, null=True)
    universities= models.ManyToManyField('main.University', blank=True, related_name='schools', help_text="Select Universities involved")
    tags        = TaggableManager()
    slug        = models.SlugField(max_length=200, unique=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(default=timezone.now, verbose_name='Posted')
    status      = models.IntegerField(choices=STATUS, default=0)


    def save(self, *args, **kwargs):
        try:
            saved_blog = Blog.objects.get(id=self.id)

            if saved_blog.image != self.image:
                img = Img.open(self.image)
                output = BytesIO()
                img.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.slug.split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        except Blog.DoesNotExist:
            if self.image == 'blog/default.jpg':
                pass

            else:
                img = Img.open(self.image)
                output = BytesIO()
                img.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.slug.split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        super(Blog, self).save(*args, **kwargs)




    def get_absolute_url(self):
        return reverse("blog:blog-detail", kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title





class Comment(models.Model):
    post    = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)
    email   = models.EmailField(max_length=100, blank=True, null=True)
    content = models.TextField(max_length=225)
    posted  = models.DateTimeField(auto_now_add=True)
    active  = models.BooleanField(default=True)
    reply   = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return f"Comment on {self.post.title}"


