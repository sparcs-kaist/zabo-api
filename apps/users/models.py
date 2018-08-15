import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.shortcuts import get_object_or_404
from apps.users.sparcssso import Client
from zabo.settings.components.secret import SSO_CLIENT_ID, SSO_SECRET_KEY, SSO_IS_BETA

sso_client = Client(SSO_CLIENT_ID, SSO_SECRET_KEY, is_beta=SSO_IS_BETA)


class ZaboUserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_superuser=is_superuser, **extra_fields)
        print("password: {pw}".format(pw=password))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def get_by_natural_key(self, email_):
        return self.get(email=email_)

    def create_user(self, email, password=None):
        return self._create_user(email, password, False, False, is_active=True)

    def create_superuser(self, email, password):
        return self._create_user(email, password, True, True, is_active=True)


# Django expects your custom user model to meet some minimum requirements. usernamefiled 정의해야함.
# 이메일 인증을 하려면 abstractbaseuser여야함.
# permission mixin은 permission 관련 method를 자동으로 추가해줌.
class ZaboUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = ZaboUserManager()
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('E', 'Etc'),
        ('B', 'Blind')
    )
    email = models.EmailField(blank=True, unique=True)
    nickName = models.CharField(max_length=20, blank=True, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER, default="B"
    )
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_sso = models.BooleanField(default=False)
    joined_date = models.DateField(auto_now_add=True)
    profile_image = models.FileField(upload_to='users/profile/', blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True)
    following = models.ManyToManyField("self", blank=True, related_name="follower", symmetrical = False)
    sid = models.CharField(max_length=30, default=0)  # 서비스에 대해 고유하게 부여받은 ID
    point = 0
    point_updated_time = None

def get_participating_zaboes(self):
    pass


def follow_other(self, nickname):
    following_user = get_object_or_404(ZaboUser, nickName=nickname)
    self.following.add(following_user)
    self.save()


def unfollow_other(self, nickname):
    following_user = get_object_or_404(ZaboUser, nickName=nickname)
    self.following.remove(following_user)
    self.save()


def get_point(self):
    self.point = sso_client.get_point(self.sid)
    return self.point


def add_point(self, delta, message):
    result = sso_client.modify_point(self.sid, delta, message, 0)
    return result
