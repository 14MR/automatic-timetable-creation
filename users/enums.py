from djchoices import DjangoChoices, ChoiceItem


class YearType(DjangoChoices):
    bachelors = ChoiceItem(0, "BS")
    masters = ChoiceItem(1, "MS")


class RoleType(DjangoChoices):
    admin = ChoiceItem(0, "Site Administrator")
    b_admin = ChoiceItem(1, "Building Administrator")
    professor = ChoiceItem(2, "Teaching Staff")
    student = ChoiceItem(3, "Student")
