from django.http import JsonResponse

from .models import SMSMessage


def delivery_webhook(request):

    message_id = request.POST.get('id')

    status = request.POST.get('status')

    sms = SMSMessage.objects.filter(
        gateway_message_id=message_id
    ).first()

    if sms:

        sms.status = status
        sms.save()

    return JsonResponse({
        'success': True
    })