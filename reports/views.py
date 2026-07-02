from django.shortcuts import (
    render,
    get_object_or_404,
)

from django.contrib.auth.decorators import login_required

from sms.models import SMSMessage
from campaigns.models import Campaign


@login_required
def delivery_dashboard(request):

    total = SMSMessage.objects.count()

    sent = SMSMessage.objects.filter(
        status='sent'
    ).count()

    failed = SMSMessage.objects.filter(
        status='failed'
    ).count()

    pending = SMSMessage.objects.filter(
        status='pending'
    ).count()

    delivery_rate = 0

    if total > 0:
        delivery_rate = round(
            (sent / total) * 100,
            2
        )

    context = {
        'total': total,
        'sent': sent,
        'failed': failed,
        'pending': pending,
        'delivery_rate': delivery_rate,
    }

    return render(
        request,
        'reports/reports_dashboard.html',
        context
    )


@login_required
def campaign_report(request, pk):

    campaign = get_object_or_404(
        Campaign,
        pk=pk
    )

    messages = SMSMessage.objects.filter(
        campaign=campaign
    )

    sent = messages.filter(
        status='sent'
    ).count()

    failed = messages.filter(
        status='failed'
    ).count()

    pending = messages.filter(
        status='pending'
    ).count()

    total = messages.count()

    delivery_rate = 0

    if total > 0:
        delivery_rate = round(
            (sent / total) * 100,
            2
        )

    return render(
        request,
        'reports/campaign_report.html',
        {
            'campaign': campaign,
            'messages': messages,
            'sent': sent,
            'failed': failed,
            'pending': pending,
            'total': total,
            'delivery_rate': delivery_rate,
        }
    )
@login_required
def dashboard(request):
    return render(request, 'reports/reports_dashboard.html')