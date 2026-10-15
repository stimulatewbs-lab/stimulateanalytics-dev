
from django.shortcuts import render
from .models import Match


def dashboard(request):
    matches = (
        Match.objects
        .filter(
            status__in=["upcoming", "live"],
            competition__is_active=True,
            competition__sport__is_active=True,
        )
        .select_related("competition", "competition__sport")
        .prefetch_related("odds")
        .order_by("kickoff")
    )

    return render(
        request,
        "bet/dashboard.html",
        {"matches": matches},
    )
