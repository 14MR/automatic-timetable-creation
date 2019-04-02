from djchoices import DjangoChoices, ChoiceItem


class SemesterType(DjangoChoices):
    fall = ChoiceItem(2, "Fall")
    spring = ChoiceItem(0, "Spring")
    summer = ChoiceItem(1, "Summer")
