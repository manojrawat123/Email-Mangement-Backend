from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
 
class CompanyUserManager(BaseUserManager):
    def create_user(self, email, company_name, company_phone ,password=None):
        """
        Creates and saves a User with the given email, name, and phone.
        
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            company_name = company_name,
            company_phone = company_phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self,  email, company_name, company_phone,  password=None, password2= None):
        """        
        Creates and saves a superuser with the given email, name, and phone. 
        """
        if password == password2:
            raise ValueError("Password Did't match")
        
        
        user = self.create_user(
            email=email,
            company_name=company_name,
            company_phone=company_phone,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CompanyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    parent_user = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',limit_choices_to={'company_admin': True})
    user_name = models.CharField(max_length=300)
    company_name = models.CharField(max_length=300)
    company_address = models.TextField()
    company_phone = models.IntegerField()
    company_desc = models.TextField()
    last_login = models.DateTimeField(null=True, blank=True)
    user_create_date = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    company_admin = models.BooleanField(default=False)
    objects = CompanyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["company_name", "company_phone"]

    def __str__(self):
        return self.company_name
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Handle permissions here (if needed)
        return True

    def has_module_perms(self, app_label):
        # Handle module permissions here (if needed)
        return True

    @property
    def is_staff(self):
        # Use the is_superuser field provided by AbstractBaseUser
        return self.is_admin