from djchoices import DjangoChoices, ChoiceItem


class DaysOfWeek(DjangoChoices):
    monday = ChoiceItem(0, "Monday")
    tuesday = ChoiceItem(1, "Tuesday")
    wednesday = ChoiceItem(2, "Wednesday")
    thursday = ChoiceItem(3, "Thursday")
    friday = ChoiceItem(4, "Friday")
    saturday = ChoiceItem(5, "Saturday")
    sunday = ChoiceItem(6, "Sunday")
