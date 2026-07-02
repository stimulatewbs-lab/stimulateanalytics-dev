import africastalking


class AfricaTalkingGateway:

    def __init__(
        self,
        username,
        api_key
    ):

        africastalking.initialize(
            username,
            api_key,
        )

        self.sms = africastalking.SMS

    def send_sms(
        self,
        phone_number,
        message
    ):

        response = self.sms.send(
            message,
            [phone_number],
        )

        return {
            "success": True,
            "response": response,
        }