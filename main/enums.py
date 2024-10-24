from enum import Enum


# Needs to map to the ids of the category types saved in the db.
class ContactTypeEnum(Enum):
    REVIEW = 1
    FEEDBACK = 2
    QUESTION = 3
    WEBSITE = 4


class ContactNotificationTypeEnum(Enum):
    EMAIL = "EMAIL"
    MOBILE = "MOBILE"
    HOME_PHONE = "HOME_PHONE"


class SystemPreferenceName(Enum):
    GST_ENABLED = "gstEnabled"
    GST_RATE = "gstRate"


class EmailConfigurationType(Enum):
    ORDER_CONFIRMATION = "ORDER_CONFIRMATION"
