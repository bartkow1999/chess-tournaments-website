from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, name, surname, username, license_number, ranking, email, password=None):
        if not name:
            raise ValueError("Users must have a name")
        if not surname:
            raise ValueError("Users must have a surname")
        if not username:
            raise ValueError("Users must have an username")
        if not license_number:
            raise ValueError("Users must have a license number")
        if not ranking:
            raise ValueError("Users must have a ranking")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            name=name,
            surname=surname,
            username=username,
            license_number=license_number,
            ranking=ranking,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, username, license_number, ranking, email, password):
        user = self.create_user(
            name=name,
            surname=surname,
            username=username,
            license_number=license_number,
            ranking=ranking,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=60, blank=False, null=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    license_number = models.CharField(max_length=30, blank=False, null=False, unique=True)
    ranking = models.IntegerField(blank=False, null=False, unique=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'username', 'license_number', 'ranking']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

