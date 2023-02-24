from django.urls import path, include
from customer import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'bankaccount', views.CustomerBankAccountViewSet)

urlpatterns = [
    path('customerviewset/', include(router.urls)),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='token_auth'),
]