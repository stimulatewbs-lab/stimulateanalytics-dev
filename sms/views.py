from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SMSForm


@login_required
def send_sms(request):

    if request.method == 'POST':

        form = SMSForm(request.POST)

        if form.is_valid():

            sms = form.save(
                commit=False
            )

            # fake sending for now
            sms.status = 'sent'
            sms.sent_at = timezone.now()

            sms.save()

            return redirect(
                'sms:sms_history'
            )

    else:

        form = SMSForm()

    return render(
        request,
        'sms/send_sms.html',
        {
            'form': form
        }
    )


@login_required
def sms_history(request):

    messages = SMSMessage.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'sms/sms_history.html',
        {
            'messages': messages
        }
    )


@login_required
def sms_detail(request, pk):

    sms = get_object_or_404(
        SMSMessage,
        pk=pk
    )

    return render(
        request,
        'sms/sms_detail.html',
        {
            'sms': sms
        }
    )