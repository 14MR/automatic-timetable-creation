import factory
import random

from users.enums import YearType
from users.models import User
from users.models import YearGroup
from users.models import Group


class YearGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = YearGroup

    year = random.uniform(2015, 2100)
    type = random.choices(YearType.choices)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    number = random.uniform(0, 10)
    study_year = factory.SubFactory(YearGroupFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("free_email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    group = factory.SubFactory(GroupFactory)
    is_admin = False
    is_active = True
