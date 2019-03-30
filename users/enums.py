from djchoices import DjangoChoices, ChoiceItem


class YearType(DjangoChoices):
    bachelors = ChoiceItem(0, "BS")
    masters = ChoiceItem(1, "MS")


class RoleType(DjangoChoices):
    admin = ChoiceItem(0, "Site Administrator")
    professor = ChoiceItem(1, "Teaching Staff")
    student = ChoiceItem(2, "Student")
    b_admin = ChoiceItem(3, "Building Administrator")
