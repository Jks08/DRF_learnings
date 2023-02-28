from django.urls import path, include
from customer import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'customerdetail', views.CustomerViewSet)
router.register(r'bankaccount', views.CustomerBankAccountViewSet, basename='bankaccount')

urlpatterns = [
    path('customerdata/', include(router.urls)),
    path('bankmaster/', views.BankMasterViewSet.as_view({'get':'list', 'post':'create'}), name='bankmaster'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='token_auth'),
]