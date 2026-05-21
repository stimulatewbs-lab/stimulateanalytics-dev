from twilio.rest import Client

from decouple import config


TWILIO_ACCOUNT_SID = config(
    'TWILIO_ACCOUNT_SID'
)

TWILIO_AUTH_TOKEN = config(
    'TWILIO_AUTH_TOKEN'
)

TWILIO_PHONE = config(
    'TWILIO_PHONE'
)


client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)


def send_twilio_sms(phone, message):

    response = client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=phone
    )

    return response