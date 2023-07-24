from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    # first_name=models.CharField(('first_name'))
    # last_name=models.CharField(('last_name'))
    username = None
    email = models.EmailField(_('email'), unique=True)
    name = models.CharField(_('name'), max_length=30, blank=True)
    phone_number = models.BigIntegerField(_('phone_number'), blank=True, null=True)
    otp = models.CharField(_('OTP'), max_length=6, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
       return self.email
    
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users', help_text='The groups this user belongs to.')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_users', help_text='Specific permissions for this user.')


class category(models.Model):
    categories = models.CharField(max_length=50)

    def __str__(self):
        return self.categories
    

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    stock = models.IntegerField(default=0)
    product_Image = models.ImageField(upload_to='product_images')
    shape = models.CharField(max_length=50)
    category = models.ForeignKey('category', on_delete=models.CASCADE)
    # is_deleted = models.BooleanField(default=False)

    # def soft_delete(self):
    #     self.is_deleted = True
    #     self.save()

    def __str__(self):
        return self.product_name


