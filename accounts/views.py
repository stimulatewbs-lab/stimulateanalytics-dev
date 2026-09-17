import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import CustomerRegistrationForm
from .models import OTPVerification


def style_form_fields(form):
    for name, field in form.fields.items():
        field.widget.attrs.update({
            "class": (
                "w-full rounded-md border border-betblack-600 "
                "bg-betblack-900 px-4 py-3 text-white "
                "focus:border-betorange-500 focus:outline-none"
            )
        })

        if name == "date_of_birth":
            field.widget.attrs.update({
                "type": "date",
                "min": "1900-01-01",
                "max": "2026-09-17",
                "style": "color-scheme: dark;",
            })

    return form


def register(request):
    form = CustomerRegistrationForm(request.POST or None)

    style_form_fields(form)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        code = OTPVerification.generate_code()

        otp = OTPVerification(
            user=user,
            channel=OTPVerification.CHANNEL_EMAIL,
            purpose=OTPVerification.PURPOSE_REGISTRATION,
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        otp.set_code(code)
        otp.save()

        send_mail(
            subject="Your BETFELLS email verification code",
            message=(
                f"Hello {user.first_name},\n\n"
                f"Your BETFELLS verification code is: {code}\n\n"
                "This code expires in 10 minutes.\n"
                "If you did not create this account, ignore this email."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        request.session["pending_otp_user_id"] = user.id

        messages.info(
            request,
            "A verification code has been sent to your email.",
        )

        return redirect("accounts:verify_email")

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def verify_email(request):
    user_id = request.session.get("pending_otp_user_id")

    if not user_id:
        messages.error(
            request,
            "Your verification session has expired. Please register again.",
        )
        return redirect("accounts:register")

    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User account not found.")
        return redirect("accounts:register")

    otp = (
        OTPVerification.objects.filter(
            user=user,
            channel=OTPVerification.CHANNEL_EMAIL,
            purpose=OTPVerification.PURPOSE_REGISTRATION,
            is_used=False,
        )
        .order_by("-created_at")
        .first()
    )

    if not otp:
        messages.error(request, "No active verification code was found.")
        return redirect("accounts:register")

    if request.method == "POST":
        code = request.POST.get("code", "").strip()

        if otp.is_expired():
            messages.error(
                request,
                "This verification code has expired.",
            )
        elif otp.attempts >= otp.max_attempts:
            messages.error(
                request,
                "Too many incorrect attempts. Please register again.",
            )
        elif not otp.check_code(code):
            otp.attempts += 1
            otp.save(update_fields=["attempts"])

            messages.error(
                request,
                "Incorrect verification code.",
            )
        else:
            otp.is_used = True
            otp.verified_at = timezone.now()
            otp.save(update_fields=["is_used", "verified_at"])

            user.customer_profile.is_email_verified = True
            user.customer_profile.save(
                update_fields=["is_email_verified"]
            )

            request.session.pop("pending_otp_user_id", None)

            login(request, user)

            messages.success(
                request,
                "Your email has been verified successfully.",
            )

            return redirect("home")

    return render(
        request,
        "accounts/verify_email.html",
        {
            "email": user.email,
        },
    )