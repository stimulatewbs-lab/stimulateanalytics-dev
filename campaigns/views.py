from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Campaign
from .forms import CampaignForm
from django.contrib.auth.decorators import login_required
@login_required
def campaign_create(request):

    form = CampaignForm(request.POST or None)

    if form.is_valid():

        campaign = form.save(commit=False)
        campaign.user = request.user
        campaign.save()

        return redirect('campaign_list')

    return render(request, 'campaigns/create.html', {
        'form': form
    })


@login_required
def campaign_update(request, pk):

    campaign = get_object_or_404(
        Campaign,
        pk=pk,
        user=request.user
    )

    form = CampaignForm(
        request.POST or None,
        instance=campaign
    )

    if form.is_valid():
        form.save()

        return redirect('campaign_list')

    return render(request, 'campaigns/update.html', {
        'form': form
    })


@login_required
def campaign_delete(request, pk):

    campaign = get_object_or_404(
        Campaign,
        pk=pk,
        user=request.user
    )

    campaign.delete()

    return redirect('campaign_list')
@login_required
def campaign_list(request):
    return render(request, 'campaigns/list.html')