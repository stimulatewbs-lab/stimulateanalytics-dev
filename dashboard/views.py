from django.shortcuts import render
from sms.models import SMSMessage
from campaigns.models import Campaign


def dashboard_view(request):

    total_sent = SMSMessage.objects.filter(
        status='sent'
    ).count()

    delivered = SMSMessage.objects.filter(
        status='delivered'
    ).count()

    total_messages = SMSMessage.objects.count()

    delivery_rate = 0

    if total_messages > 0:
        delivery_rate = round(
            (delivered / total_messages) * 100,
            1
        )

    active_campaigns = Campaign.objects.filter(
        status='active'
    ).count()

    context = {
        'total_sent': total_sent,
        'delivery_rate': delivery_rate,
        'active_campaigns': active_campaigns,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )