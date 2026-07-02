from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Campaign
from .forms import CampaignForm
from .models import ContactGroup
from .forms import ContactGroupForm

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.all()

    return render(
        request,
        "campaigns/campaign_list.html",
        {"campaigns": campaigns},
    )


@login_required
def campaign_create(request):
    if request.method == "POST":
        form = CampaignForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("campaigns:campaign_list")
    else:
        form = CampaignForm()

    return render(
        request,
        "campaigns/campaign_form.html",
        {"form": form},
    )


@login_required
def campaign_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == "POST":
        form = CampaignForm(
            request.POST,
            instance=campaign,
        )

        if form.is_valid():
            form.save()
            return redirect("campaigns:campaign_list")
    else:
        form = CampaignForm(instance=campaign)

    return render(
        request,
        "campaigns/campaign_form.html",
        {"form": form},
    )


@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    if request.method == "POST":
        campaign.delete()
        return redirect("campaigns:campaign_list")

    return render(
        request,
        "campaigns/campaign_confirm_delete.html",
        {"campaign": campaign},
    )