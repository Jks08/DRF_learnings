from rest_framework import status, permissions, authentication, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import renderer_classes
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
        # Only authenticated users can create a bank account.
        if not self.request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CustomerBankAccount.objects.filter(customer=self.request.user, is_active=True)
        else:
            return CustomerBankAccount.objects.none()
        
    def update(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)