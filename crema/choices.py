from enum import Enum


class EventType(Enum):
    # PSCORE
    USER = "USER"
    LOAN_APPLICATION = "LOAN_APPLICATION"
    DOCUMENT = "DOCUMENT"
    LOAN = "LOAN"
    USER_INFO_REQUEST = "USER_INFO_REQUEST"
    EMPLOYMENT = "EMPLOYMENT"
    DEBIT_INSTRUCTION = "DEBIT_INSTRUCTION"
    ADDRESS = "ADDRESS"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    INCOME_VERIFICATION = "INCOME_VERIFICATION"
    USER_REFERENCES = "USER_REFERENCES"
    ASSISTANCE_REMINDER = "ASSISTANCE_REMINDER"
    ASSISTANCE_ACTIVITY = "ASSISTANCE_ACTIVITY"
    WHATSAPP_COMM = "WHATSAPP_COMM"

    # AMS
    ASSESSMENT = "ASSESSMENT"

    # USER_ACTIVITY
    USER_ACTIVITY = "USER_ACTIVITY"

    # PAYMENTS
    LOAN_INFO = "LOAN_INFO"
    LOAN_DATA = "LOAN_DATA"
    VIRTUAL_ACCOUNT = "VIRTUAL_ACCOUNT"

    # INTERNAL TOPICS
    # All internal topics start with prefix I_
    I_LOAN_APPLICATION_INDEX = "I_LOAN_APPLICATION_INDEX"
    I_LEAD_INDEX = "I_LEAD_INDEX"
    I_MESSAGE_INDEX = "I_MESSAGE_INDEX"


class EventPartition(Enum):
    # PSCORE
    USER = 64
    LOAN_APPLICATION = 64
    DOCUMENT = 64
    LOAN = 64
    USER_INFO_REQUEST = 64
    EMPLOYMENT = 64
    DEBIT_INSTRUCTION = 64
    ADDRESS = 64
    BANK_ACCOUNT = 64
    INCOME_VERIFICATION = 64
    USER_REFERENCES = 64
    ASSISTANCE_REMINDER = 64
    ASSISTANCE_ACTIVITY = 64
    WHATSAPP_COMM = 64

    # AMS
    ASSESSMENT = 64
    PRODUCT_ELIGIBILITY = 64

    # USER_ACTIVITY
    USER_ACTIVITY = 256

    # PAYMENTS
    LOAN_INFO = 64
    LOAN_DATA = 64
    VIRTUAL_ACCOUNT = 64

    # INTERNAL TOPICS
    I_LOAN_APPLICATION_INDEX = 256
    I_LEAD_INDEX = 256
    I_MESSAGE_INDEX = 128
