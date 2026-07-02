from datetime import datetime


class MockGateway:

    def send_sms(
        self,
        phone_number,
        message
    ):

        print(
            f"SMS SENT TO: {phone_number}"
        )

        print(
            f"MESSAGE: {message}"
        )

        return {
            "success": True,
            "provider_id": "MOCK001",
            "sent_at": datetime.now(),
        }