from pydantic import BaseModel


class SmsServiceConfig(BaseModel):
    api_key: str
    debug: bool = False


class SmsService:
    def __init__(self, config: SmsServiceConfig):
        self.config = config

    def send_sms(self, phone: str, message: str):
        if self.config.debug:
            print(f"Sending SMS to {phone}: {message}")
        else:
            # TODO: Алексей: Initialize the SMS client using the API key from the config
            ...
