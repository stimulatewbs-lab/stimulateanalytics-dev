import africastalking

from decouple import config


username = config(
    'AT_USERNAME'
)

api_key = config(
    'AT_API_KEY'
)

africastalking.initialize(
    username,
    api_key
)

sms = africastalking.SMS


def send_africastalking_sms(phone, message):

    response = sms.send(
        message,
        [phone]
    )

    return response