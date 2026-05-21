from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Wallet
from .models import Transaction


def billing(request):

    wallet = Wallet.objects.filter(
        user=request.user
    ).first()

    transactions = Transaction.objects.filter(
        wallet=wallet
    ).order_by('-created_at')

    context = {
        'wallet': wallet,
        'transactions': transactions
    }

    return render(
        request,
        'billing/index.html',
        context
    )