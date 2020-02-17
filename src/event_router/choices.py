from djchoices import ChoiceItem, DjangoChoices


class EventType(DjangoChoices):
    USER = ChoiceItem("USER")
    LOAN_APPLICATION = ChoiceItem("LOAN_APPLICATION")
    ENTITY = ChoiceItem("ENTITY")
    DOCUMENT = ChoiceItem("DOCUMENT")
    LENDER_LOAN_DATA = ChoiceItem("LENDER_LOAN_DATA")
    ASSESSMENT = ChoiceItem("ASSESSMENT")
