

# Create your views here.
from django.shortcuts import render
from .models import DeliveryReport


def reports(request):

    logs = DeliveryReport.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'reports/index.html',
        {'logs': logs}
    )