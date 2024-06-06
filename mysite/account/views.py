from django.shortcuts import render
from rest_framework import generics
from .serializers import AccountSerializer
from .models import Account

# Create your views here.

# Create your views here.

def index(request):
    return render(request, 'index.html')


class AccountAPIList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountAPIUpdate(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountAPIDestroy(generics.DestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer