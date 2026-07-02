from sms.gateways.mock import MockGateway


class SMSService:

    def __init__(self):

        self.gateway = MockGateway()

    def send(
        self,
        sms_message
    ):

        response = self.gateway.send_sms(
            sms_message.contact.phone_number,
            sms_message.message,
        )

        return response