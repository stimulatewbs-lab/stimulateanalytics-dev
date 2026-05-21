from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from campaigns.models import Campaign
from contacts.models import Contact


@login_required
def dashboard_view(request):

    total_campaigns = Campaign.objects.filter(user=request.user).count()

    total_contacts = Contact.objects.filter(group__user=request.user).count()

    context = {
        'total_campaigns': total_campaigns,
        'total_contacts': total_contacts,
    }

    return render(request, 'dashboard/index.html', context)