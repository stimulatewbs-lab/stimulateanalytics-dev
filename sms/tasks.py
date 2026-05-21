from celery import shared_task

from .services.twilio_service import send_twilio_sms

from .models import SMSMessage


@shared_task
def send_sms_task(sms_id):

    sms = SMSMessage.objects.get(id=sms_id)

    response = send_twilio_sms(
        sms.phone,
        sms.message
    )

    sms.gateway_message_id = response.sid
    sms.status = 'sent'

    sms.save()

    return True