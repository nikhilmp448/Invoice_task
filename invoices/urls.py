from django.urls import path

from .views import InvoiceViewSet, InvoiceDetailViewSet

urlpatterns = [
    path('invoices/', InvoiceViewSet.as_view(), name='invoices'),
    path('invoices/<int:pk>/', InvoiceDetailViewSet.as_view(), name='invoice_detail'),
]