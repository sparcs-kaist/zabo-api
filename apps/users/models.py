import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ZaboUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser,  **extra_fields):
        user =  self.model(email = email,
                is_staff = is_staff,
                is_superuser = is_superuser,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password, False, False, is_active=False)

    def create_superuser(self, email, password):
        return self._create_user(email, password, True, True, is_active=True)



class ZaboUser(AbstractBaseUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    joined_date = models.DateField(auto_now_add=True)
    profile_image = models.FileField(upload_to='users/profile/')
    phone = models.CharField(max_length=45, blank=True)

