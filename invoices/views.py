from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice,InvoiceDetail
from .serializers import InvoiceSerializer,InvoiceDetailSerializer

class InvoiceViewSet(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invoice = serializer.save()

        # Create invoice details from the payload
        invoice_details = request.data.get('invoice_details', [])
        for invoice_detail in invoice_details:
            invoice_detail_serializer = InvoiceDetailSerializer(data=invoice_detail)
            invoice_detail_serializer.is_valid(raise_exception=True)

            invoice_detail = invoice_detail_serializer.save()
            invoice_detail.invoice = invoice
            invoice_detail.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class InvoiceDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer