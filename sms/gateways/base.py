class BaseGateway:

    def send_sms(
        self,
        phone_number,
        message
    ):
        raise NotImplementedError