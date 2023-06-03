from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


import sys
from PIL import Image as Img
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, is_staff, is_admin, is_superuser):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        now 	= timezone.now()
        email 	= self.normalize_email(email)
        user 	= self.model(
		    email=email,
		    username=username,
		    is_staff=is_staff,
		    is_active=True,
		    is_superuser=is_superuser,
		    is_admin=is_admin,
		    last_login=now,
		    date_joined=now,
		)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password, False, False, False)

    def create_superuser(self, email, username, password):
        user = self._create_user(email, username, password, True, True, True)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email 			= models.EmailField(max_length=100, unique=True)
    username 		= models.CharField(max_length=100, null=True, blank=True)
    is_staff 		= models.BooleanField(default=False)
    is_admin 		= models.BooleanField(default=False)
    is_superuser 	= models.BooleanField(default=False)
    is_active 		= models.BooleanField(default=True)
    last_login 		= models.DateTimeField(null=True, blank=True)
    date_joined	 	= models.DateTimeField(auto_now_add=True)
    first_name 		= models.CharField(max_length=100)
    last_name 		= models.CharField(max_length=100)


    USERNAME_FIELD 	= 'email'
    EMAIL_FIELD 	= 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def get_absolute_url(self):
        return "/account/%i/" % (self.pk)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user', default='user/default.jpg')
    is_artist = models.BooleanField(default=False, help_text='Select if user is an Artist')
    artist_user = models.ForeignKey('artist.Artist', on_delete=models.DO_NOTHING, blank=True, null=True, help_text='Select for Artists')

    def save(self, *args, **kwargs):
        try:
            saved_profile = UserProfile.objects.get(id=self.id)

            if saved_profile.image != self.image:
                img = Img.open(self.image)
                img = img.convert("RGB")
                output = BytesIO()
                new_image = img.resize((200, 200))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.user.username.lower().split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        except UserProfile.DoesNotExist:
            if self.image == 'user/default.jpg':
                pass

            else:
                img = Img.open(self.image)
                img = img.convert("RGB")
                output = BytesIO()
                new_image = img.resize((200, 200))
                new_image.save(output, format='JPEG', quality=60)
                output.seek(0)
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.user.username.lower().split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        super(UserProfile, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "User Profiles"


    def __str__(self):
        return f"{ self.user.username } Profile"






class Subscriber(models.Model):
    email 		= models.EmailField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription by {self.email}"


