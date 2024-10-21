import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError


# Phone validation service specific to Australia (AU).
MOBILE_FORMAT_ERROR = "Please enter your mobile in the format: +614XXXXXXXX or 04XXXXXXXX."
LANDLINE_FORMAT_ERROR = "Please enter your home landline phone in the correct format. (eg. 08XXXXXXXX, 02XXXXXXXX)"


def validate_mobile(mobile) -> str:
    return validate_phone_number(mobile, phonenumbers.PhoneNumberType.MOBILE)


def validate_landline(landline) -> str:
    return validate_phone_number(landline, phonenumbers.PhoneNumberType.FIXED_LINE)


def validate_phone_number(phone_number: str, phone_type: int) -> str:
    if phone_number is not None and phone_number != '':
        try:
            parsed_landline = phonenumbers.parse(phone_number, "AU")
            if not phonenumbers.is_valid_number(parsed_landline):
                raise ValidationError(get_phone_format_error(phone_type))
            if not phonenumbers.number_type(parsed_landline) == phone_type:
                raise ValidationError(get_phone_format_error(phone_type))

            return format_phone_number(str(parsed_landline.country_code) + str(parsed_landline.national_number))
        except NumberParseException:
            raise ValidationError(get_phone_format_error(phone_type))

    return format_phone_number(phone_number)


def get_phone_format_error(phone_type: int) -> str:
    if phone_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        return LANDLINE_FORMAT_ERROR
    elif phone_type == phonenumbers.PhoneNumberType.MOBILE:
        return MOBILE_FORMAT_ERROR

    return "Unexpected Phone Type"


# provide a consistent format when saving to the db
def format_phone_number(phone_number):
    if phone_number is None or phone_number.strip() == '':
        return None

    return f"+{phone_number}"
