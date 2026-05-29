from django.shortcuts import render, redirect, get_object_or_404
from .models import Campaign


def campaign_list(request):
    campaigns = Campaign.objects.all()

    return render(
        request,
        'campaigns/campaign_list.html',
        {'campaigns': campaigns}
    )


def campaign_create(request):

    if request.method == 'POST':

        name = request.POST.get('name')

        Campaign.objects.create(
            name=name,
            user=request.user
        )

        return redirect('campaign_list')

    return render(
        request,
        'campaigns/create.html'
    )


def campaign_update(request, pk):

    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST':

        campaign.name = request.POST.get('name')
        campaign.save()

        return redirect('campaign_list')

    return render(
        request,
        'campaigns/update.html',
        {'campaign': campaign}
    )


def campaign_delete(request, pk):

    campaign = get_object_or_404(Campaign, pk=pk)

    campaign.delete()

    return redirect('campaign_list')
