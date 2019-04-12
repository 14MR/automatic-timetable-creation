from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from users.enums import YearType, RoleType


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Enter email")
        if not password:
            raise ValueError("Enter password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email address", max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=150)
    role = models.PositiveSmallIntegerField(choices=RoleType.choices, default=RoleType.student)
    group = models.ForeignKey("Group", blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_staff(self):
        return self.is_superuser


class YearGroup(models.Model):
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2100)]
    )
    type = models.PositiveSmallIntegerField(verbose_name='type of group', choices=YearType.choices)

    def __str__(self):
        return f"{self.get_type_display()}{self.year}"


class Group(models.Model):
    number = models.PositiveSmallIntegerField()
    study_year = models.ForeignKey(YearGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.study_year}-{self.number}"
