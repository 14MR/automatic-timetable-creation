import factory
import random

from users.models import User
from users.models import Role
from users.models import YearGroup
from users.models import Group


class YearGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = YearGroup

    year = random.randint(2015, 2100)
    type = random.choice([0, 1])


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    number = random.randint(0, 10)
    study_year = factory.SubFactory(YearGroupFactory)


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    level = random.randint(0, 3)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("free_email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = factory.SubFactory(RoleFactory)
    group = factory.SubFactory(GroupFactory)
    is_admin = False
    is_active = True
