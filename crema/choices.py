from enum import Enum


class EventType(Enum):
    USER = "USER"
    LOAN_APPLICATION = "LOAN_APPLICATION"
    ENTITY = "ENTITY"
    DOCUMENT = "DOCUMENT"
    LENDER_LOAN_DATA = "LENDER_LOAN_DATA"
    ASSESSMENT = "ASSESSMENT"
