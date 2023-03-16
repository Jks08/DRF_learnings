from rest_framework import status, permissions, authentication, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import renderer_classes
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from typing import List
import json

from customer.models import Customer, CustomerBankAccount, BankMaster
from customer.serializers import CustomerSerializer, CustomerBankAccountSerializer, BankMasterSerializer
from customer.filters import CustomerFilter, CustomerBankAccountFilter

# Create your views here.

class CustomAuthToken(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
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

    def get_permissions(self) -> List[permissions.BasePermission]:
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> Customer:
        if self.action == 'create':
            return Customer.objects.none()
        elif self.request.user.is_authenticated:
            return Customer.objects.filter(id=self.request.user.id)
        else:
            return Customer.objects.none()

    def get_object(self) -> Customer:
        if self.action == 'create':
            return None
        else:
            return self.request.user


class CustomerBankAccountViewSet(viewsets.ModelViewSet):
    queryset = CustomerBankAccount.objects.all()
    serializer_class = CustomerBankAccountSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs) -> Response:
        if not self.request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.set_cookie('bank_account_data', json.dumps(serializer.data))
            return response

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                accdata = request.COOKIES.get('bank_account_data')
                accdata = json.loads(accdata)
                return Response(accdata)
            except:
                # serializer = self.get_serializer(self.customer_bank_account(), many=True)
                # return Response(serializer.data)
                return Response({'Your session has expired, please send a POST request again. (The cookie does not exist)'})
            
    def customer_bank_account(self) -> CustomerBankAccount:
        return self.queryset.filter(customer=self.request.user, is_active = True)
        
    def update(self, request, *args, **kwargs) -> Response:
        if not self.request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        
class BankMasterViewSet(viewsets.ModelViewSet):
    queryset = BankMaster.objects.all()
    serializer_class = BankMasterSerializer

    def get_permissions(self) -> List[permissions.BasePermission]:
        if self.action == 'create' or self.action=='update':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)
