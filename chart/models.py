from django.db import models
from account.models import User
from main.models import University


import sys
from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime



def today_utc():
    return datetime.utcnow().date()


CHART_STATUS = (
    (0,"Not Charting"),
    (1,"Charting"),
)

REVIEW_STATUS = (
    (0,"In Review"),
    (1,"Accepted"),
    (2,"Denied")
)


class Track(models.Model):
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, help_text='Optional')
    title       = models.CharField(max_length=150, verbose_name='Track title')
    slug        = models.SlugField(max_length=200, unique=True, blank=True, null=True, help_text='Click on the title field to populate this field')
    artist      = models.CharField(max_length=150)
    artist_tag  = models.ManyToManyField('artist.Artist', blank=True, related_name='artists', verbose_name='Artist Tag', help_text='Optional:Tag artist and producers')
    university  = models.ManyToManyField('main.University', related_name='institution')
    link        = models.CharField(max_length=200, blank=True, null=True, verbose_name='Song Link', help_text='Optional')
    description = models.TextField(max_length=225, blank=True, null=True, verbose_name='Song Description', help_text='Optional')
    artwork     = models.ImageField(upload_to='artwork', default='artwork/default.jpg')
    zgm_rank    = models.IntegerField(verbose_name='ZGM Rank', blank=True, null=True, unique=True)
    uni_rank    = models.IntegerField(verbose_name='University Rank', blank=True, null=True)
    released    = models.DateField(default=today_utc)
    submission  = models.IntegerField(choices=REVIEW_STATUS, default=0, verbose_name='Submission Status')
    status      = models.IntegerField(choices=CHART_STATUS, default=0, verbose_name='Chart Status')


    def save(self, *args, **kwargs):
        try:
            saved_track = Track.objects.get(id=self.id)

            if saved_track.artwork != self.artwork:
                img = Img.open(self.artwork)
                img = img.convert("RGB")
                output = BytesIO()
                new_image = img.resize((500, 500))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.artwork = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.title.lower().split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        except Track.DoesNotExist:
            if self.artwork == 'artwork/default.jpg':
                pass

            else:
                img = Img.open(self.artwork)
                img = img.convert("RGB")
                output = BytesIO()
                new_image = img.resize((500, 500))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.artwork = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.title.lower().split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        super(Track, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-released']
