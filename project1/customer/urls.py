from django.urls import path, include
from customer import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('customerviewset/', include(router.urls)),
    path('create/', views.CustomerCreateView.as_view(), name='create'),
    path('list/', views.CustomerListView.as_view(), name='list'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='token_auth'),

]