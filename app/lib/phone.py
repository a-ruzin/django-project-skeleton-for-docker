import phonenumbers
from phonenumbers import PhoneNumberFormat


def normalize_phone(phone_number: str, country: str = "RU") -> str | None:
    try:
        parsed = phonenumbers.parse(phone_number, country)

        normalized = phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        return normalized
    except phonenumbers.NumberParseException:
        return None
