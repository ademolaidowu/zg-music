from django.db import models
from account.models import User

import sys
from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile



STATUS = (
    (0,"In Review"),
    (1,"Confirmed"),
    (2,"Denied"),
    (3,"Graduate")
)


class ArtistCategory(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title





class Artist(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name            = models.CharField(max_length=150, verbose_name='Stage Name')
    slug            = models.SlugField(max_length=200, unique=True, blank=True, null=True, help_text='Click on the name field to populate this field')
    category        = models.ManyToManyField('ArtistCategory', blank=True, related_name='genre')
    university      = models.ForeignKey('main.University', on_delete=models.CASCADE, blank=True, null=True)
    image           = models.ImageField(upload_to='artist', default='artist/default.jpg')
    paid            = models.BooleanField(default=False, verbose_name='Artist Payment', help_text='Select if payment has been made to activate full artist card features')
    verified        = models.BooleanField(default=False)
    status          = models.IntegerField(choices=STATUS, default=0)

    ig_page         = models.CharField(max_length=200, null=True, blank=True, verbose_name='Instagram account', help_text='Required')
    twitter_page    = models.CharField(max_length=200, null=True, blank=True, verbose_name='Twitter account', help_text='Optional')

    itunes          = models.CharField(max_length=200, null=True, blank=True, verbose_name='iTunes Profile', help_text='Optional')
    audiomack       = models.CharField(max_length=200, null=True, blank=True, verbose_name='Audiomack Profile', help_text='Optional')
    soundcloud      = models.CharField(max_length=200, null=True, blank=True, verbose_name='Soundcloud Profile', help_text='Optional')


    def save(self, *args, **kwargs):
        try:
            saved_artist = Artist.objects.get(id=self.id)

            if saved_artist.image != self.image:
                img = Img.open(self.image)
                img = img.convert("RGB")
                output = BytesIO()
                new_image = img.resize((200, 200))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.name.lower().split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        except Artist.DoesNotExist:
            if self.image == 'artist/default.jpg':
                pass

            else:
                img = Img.open(self.image)
                img = img.convert("RGB")
                output = BytesIO()
                new_image = img.resize((200, 200))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.name.lower().split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        super(Artist, self).save(*args, **kwargs)



    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name



