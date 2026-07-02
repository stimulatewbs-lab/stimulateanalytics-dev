from twilio.rest import Client


class TwilioGateway:

    def __init__(
        self,
        sid,
        token,
        sender
    ):

        self.client = Client(
            sid,
            token
        )

        self.sender = sender

    def send_sms(
        self,
        phone_number,
        message
    ):

        response = self.client.messages.create(
            body=message,
            from_=self.sender,
            to=phone_number,
        )

        return {
            "success": True,
            "provider_id": response.sid,
        }