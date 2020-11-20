from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from artigo.models import Produto, TipoDeProduto
from django.conf import settings
from django.db.models.signals import post_save


# Create your models here.

class ManagerDoUsuario(BaseUserManager):

    def create_user(self, first_name, last_name, telephone, nusp, email, password=None):
        if not first_name:
            raise ValueError("O usuário precisa fornecer um nome")
        if not last_name:
            raise ValueError("O usuário precisa fornecer um sobrenome")
        if not telephone:
            raise ValueError("O usuário precisa fornecer um número de telefone")
        if not nusp:
            raise ValueError("O usuário precisa fornecer um número USP")
        if not email:
            raise ValueError("O usuário precisa fornecer um email")

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            telephone = telephone,
            nusp = nusp,
            email = self.normalize_email(email),
            )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, nusp, telephone, password):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            nusp = nusp,
            telephone = telephone,
            email = self.normalize_email(email),
            password = password,
            )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    first_name      = models.CharField(max_length=40)
    last_name       = models.CharField(max_length=40)
    nusp            = models.CharField(max_length=8, unique=True)
    telephone       = models.CharField(max_length=11, unique=True, validators=[RegexValidator(regex='^.{11}$', message="O telefone precisa ter 11 números")])
    email           = models.CharField(max_length=60, unique=True)
    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_atleta       = models.BooleanField(default=True)
    is_professor    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    #meus_alugueis   = models.ManyToManyField(TipoDeProduto, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'nusp', 'telephone']

    objects = ManagerDoUsuario()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
        
    def has_module_perms(self, app_label):
        return True

""" def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Usuario.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=Usuario) """




