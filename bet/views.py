
from django.shortcuts import render
from .models import Match


import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Bet, BetSelection, Match, MatchOdds
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
def place_bet(request):
    # Only authenticated users can place bets.
    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "Please log in to place a bet."},
            status=401,
        )

    # Parse the JSON submitted by the existing betslip.
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"success": False, "message": "Invalid request data."},
            status=400,
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {"success": False, "message": "Invalid bet data."},
            status=400,
        )

    try:
        stake = Decimal(str(data.get("stake", "")))
    except (InvalidOperation, ValueError):
        return JsonResponse(
            {"success": False, "message": "Enter a valid stake."},
            status=400,
        )

    if not stake.is_finite() or stake <= 0:
        return JsonResponse(
            {"success": False, "message": "Stake must be greater than zero."},
            status=400,
        )

    # Match the precision and capacity of Bet.stake.
    if stake.as_tuple().exponent < -2 or stake >= Decimal("10000000000"):
        return JsonResponse(
            {"success": False, "message": "Stake must have at most two decimal places."},
            status=400,
        )

    selections = data.get("selections")

    if not isinstance(selections, list) or not selections:
        return JsonResponse(
            {"success": False, "message": "Add at least one selection to your betslip."},
            status=400,
        )

    if len(selections) > 50:
        return JsonResponse(
            {"success": False, "message": "Too many selections in one bet."},
            status=400,
        )

    allowed_selections = {
        "home_win": "Home Win",
        "draw": "Draw",
        "away_win": "Away Win",
    }

    # Validate the submitted selections before saving anything.
    validated = []
    seen_matches = set()
    total_odds = Decimal("1.00")

    for item in selections:
        if not isinstance(item, dict):
            return JsonResponse(
                {"success": False, "message": "Invalid selection data."},
                status=400,
            )

        match_id = item.get("match_id")
        selection_key = item.get("selection")
        market = item.get("market", "match_result")

        if (
            not isinstance(match_id, int)
            or isinstance(match_id, bool)
            or match_id <= 0
            or market != "match_result"
            or selection_key not in allowed_selections
        ):
            return JsonResponse(
                {"success": False, "message": "Invalid match or selection."},
                status=400,
            )

        if match_id in seen_matches:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Only one selection per match is currently supported.",
                },
                status=400,
            )

        seen_matches.add(match_id)

        match = (
            Match.objects
            .filter(
                pk=match_id,
                status=Match.Status.UPCOMING,
                kickoff__gt=timezone.now(),
                competition__is_active=True,
                competition__sport__is_active=True,
            )
            .first()
        )

        if match is None:
            return JsonResponse(
                {
                    "success": False,
                    "message": "A selected match is unavailable for betting.",
                },
                status=400,
            )

        odds_record = (
            MatchOdds.objects
            .filter(match=match, is_active=True)
            .order_by("-updated_at", "-pk")
            .first()
        )

        if odds_record is None:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Odds are unavailable for a selected match.",
                },
                status=400,
            )

        odds_field = selection_key
        odds_value = getattr(odds_record, odds_field)

        if not odds_value.is_finite() or odds_value <= 1:
            return JsonResponse(
                {
                    "success": False,
                    "message": "The odds for a selected outcome are invalid.",
                },
                status=400,
            )

        validated.append({
            "match": match,
            "market": "match_result",
            "selection": allowed_selections[selection_key],
            "odds": odds_value,
        })

        total_odds *= odds_value

    potential_payout = (stake * total_odds).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    if potential_payout >= Decimal("1000000000000"):
        return JsonResponse(
            {"success": False, "message": "Potential payout exceeds the allowed limit."},
            status=400,
        )

    # Save the bet and all its selections as one transaction.
    with transaction.atomic():
        bet = Bet.objects.create(
            user=request.user,
            bet_type=(
                Bet.BetType.SINGLE
                if len(validated) == 1
                else Bet.BetType.MULTIPLE
            ),
            stake=stake,
            potential_payout=potential_payout,
        )

        BetSelection.objects.bulk_create([
            BetSelection(
                bet=bet,
                match=item["match"],
                market=item["market"],
                selection=item["selection"],
                odds_at_placement=item["odds"],
            )
            for item in validated
        ])

    return JsonResponse(
        {
            "success": True,
            "message": "Bet placed successfully.",
            "bet_id": bet.pk,
            "stake": str(bet.stake),
            "potential_payout": str(bet.potential_payout),
            "status": bet.status,
        },
        status=201,
    )
