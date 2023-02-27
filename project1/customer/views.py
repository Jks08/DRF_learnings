from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import models
from rest_framework import status, permissions, authentication, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import mixins, generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from customer.models import Customer, CustomerBankAccount, BankMaster
from customer.serializers import CustomerSerializer, CustomerBankAccountSerializer, BankMasterSerializer
from customer.filters import CustomerFilter, CustomerBankAccountFilter

# Create your views here.

class CustomAuthToken(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            serializer = CustomerSerializer(user)
            return Response({
                'token': token.key,
                # 'user': serializer.data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [authentication.TokenAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]   
    filterset_class = CustomerFilter
    search_fields = ['email', 'first_name', 'last_name', 'pan_no']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == 'create':
            return Customer.objects.none()
        elif self.request.user.is_authenticated:
            return Customer.objects.filter(id=self.request.user.id)
        else:
            return Customer.objects.none()

    def get_object(self):
        if self.action == 'create':
            return None
        else:
            return self.request.user

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class CustomerBankAccountViewSet(viewsets.ModelViewSet):
    queryset = CustomerBankAccount.objects.all()
    serializer_class = CustomerBankAccountSerializer
    authentication_classes = [authentication.TokenAuthentication]
    
    def create(self, request, *args, **kwargs):
        customer = request.user
        if customer.is_authenticated:
            if customer.customerbankaccount_set.count() < 4:
                return super().create(request, *args, **kwargs)
            else:
                return Response({'error': 'Maximum number of bank accounts reached'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        customer = self.request.user
        id = self.kwargs.get('id')
        if customer.is_authenticated:
            if id:
                return CustomerBankAccount.objects.filter(customer=customer, id=id)
            return CustomerBankAccount.objects.filter(customer=customer, is_active=True)
        else:
            return CustomerBankAccount.objects.none()
        
    def perform_create(self, serializer):
        customer = self.request.user
        if customer.is_authenticated:
            account_number = self.request.data.get('account_number')
            if CustomerBankAccount.objects.filter(customer=customer, account_number=account_number, bank=self.request.data.get('bank')).exists():
                return Response({'error': 'Bank account already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(customer=customer, is_active=True)
                CustomerBankAccount.objects.filter(customer=customer).exclude(account_number=account_number).update(is_active=False)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        customer = request.user
        if customer.is_authenticated:
            account_number = self.request.data.get('account_number')
            if CustomerBankAccount.objects.filter(customer=customer, account_number=account_number).exists():
                return super().update(request, *args, **kwargs)
            else:
                return Response({'error': 'Bank account does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, *args, **kwargs):
        customer = request.user
        if customer.is_authenticated:
            account_number = self.request.data.get('account_number')
            if CustomerBankAccount.objects.filter(customer=customer, account_number=account_number).exists():
                return super().partial_update(request, *args, **kwargs)
            else:
                return Response({'error': 'Bank account does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)