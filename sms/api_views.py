from rest_framework.views import APIView
from rest_framework.response import Response

from .models import SMSMessage


class SMSListAPI(APIView):

    def get(self, request):

        sms = SMSMessage.objects.all()

        data = []

        for item in sms:

            data.append({
                'phone': item.phone,
                'message': item.message,
                'status': item.status,
            })

        return Response(data)