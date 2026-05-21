

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from contacts.models import Contact
from contacts.models import ContactGroup

from .forms import SendSMSForm
from .models import SMSMessage
from .tasks import send_sms_task


def sms_dashboard(request):

    total_sms = SMSMessage.objects.count()

    delivered = SMSMessage.objects.filter(
        status='delivered'
    ).count()

    failed = SMSMessage.objects.filter(
        status='failed'
    ).count()

    context = {
        'total_sms': total_sms,
        'delivered': delivered,
        'failed': failed,
    }

    return render(
        request,
        'sms/dashboard.html',
        context
    )


def send_sms(request):

    form = SendSMSForm(request.POST or None)

    if form.is_valid():

        sender_id = form.cleaned_data['sender_id']
        group = form.cleaned_data['group']
        message = form.cleaned_data['message']

        contacts = Contact.objects.filter(
            group=group
        )

        for contact in contacts:

            sms = SMSMessage.objects.create(
                user=request.user,
                contact=contact,
                sender_id=sender_id,
                phone=contact.phone,
                message=message,
                status='pending'
            )
            send_sms_task.delay(sms.id) 
        messages.success(
            request,
            'SMS queued successfully.'
        )

        return redirect('sms_history')

    return render(
        request,
        'sms/send.html',
        {'form': form}
    )


def sms_history(request):

    sms_logs = SMSMessage.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'sms/history.html',
        {'sms_logs': sms_logs}
    )