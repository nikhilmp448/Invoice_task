from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_invoice(self):
        data = {
            "invoice_id": "1",
            "invoice_details": [
                {
                    "description": "Product A",
                    "quantity": 5,
                    "unit_price": 10.0,
                    "price": 5
                }
            ]
        }

        response = self.client.post("invoices/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.first().invoice.invoice_id, "1")
    
    def test_retrieve_invoice(self):
        invoice = Invoice.objects.create(invoice_number="2")
        InvoiceDetail.objects.create(invoice=invoice, description="Product B", quantity=3, unit_price=15.0, price = 5)

        response = self.client.get(f"invoices/{invoice.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["invoice_number"], "2")
        self.assertEqual(len(response.data["invoice_details"]), 1)
    
    def test_update_invoice_detail(self):
        invoice = Invoice.objects.create(invoice_number="3")
        invoice_detail = InvoiceDetail.objects.create(invoice=invoice, description="Product C", quantity=2, unit_price=20.0, price = 5)

        updated_data = {
            "description": "Updated Product C",
            "quantity": 3,
            "unit_price": 25.0
        }

        response = self.client.put(f"/invoice-details/{invoice_detail.pk}/", updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InvoiceDetail.objects.get(pk=invoice_detail.pk).description, "Updated Product C")
    
    def test_delete_invoice(self):
        invoice = Invoice.objects.create(invoice_number="4")

        response = self.client.delete(f"/invoices/{invoice.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

    def test_list_invoices(self):
        Invoice.objects.create(invoice_number="5")
        Invoice.objects.create(invoice_number="6")

        response = self.client.get("/invoices/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_invoice_details(self):
        invoice = Invoice.objects.create(invoice_number="7")
        InvoiceDetail.objects.create(invoice=invoice, description="Product D", quantity=4, unit_price=30.0, price = 5)

        response = self.client.get(f"/invoice-details/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
