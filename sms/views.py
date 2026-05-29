from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import SMSMessage


@login_required
def sms_dashboard(request):

    recent_messages = SMSMessage.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]

    context = {
        'recent_messages': recent_messages
    }

    return render(
        request,
        'sms/dashboard.html',
        context
    )


@login_required
def send_sms(request):

    if request.method == 'POST':

        recipient = request.POST.get('recipient')

        message = request.POST.get('message')

        sender_id = request.POST.get('sender_id')

        SMSMessage.objects.create(
            user=request.user,
            recipient=recipient,
            message=message,
            sender_id=sender_id,
            status='pending'
        )

        return redirect('sms_history')

    return render(
        request,
        'sms/send.html'
    )


@login_required
def sms_history(request):

    messages = SMSMessage.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        'messages': messages
    }

    return render(
        request,
        'sms/history.html',
        context
    )