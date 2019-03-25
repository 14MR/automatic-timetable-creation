from djchoices import DjangoChoices, ChoiceItem


class YearType(DjangoChoices):
    bachelors = ChoiceItem(0, 'BS')
    masters = ChoiceItem(1, 'MS')
