from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vendors.models import Vendor,VendorProduct
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class VendorUserTests(APITestCase):

    def setUp(self):
        # Create vendor user, vendor, and product
        self.vendor_user = CustomUser.objects.create_user(username="vendoruser", password="password", is_vendor=True)
        self.client.login(username="vendoruser", password="password")
        self.vendor = Vendor.objects.create(name="Test Vendor", user=self.vendor_user)
        self.product = VendorProduct.objects.create(
            name="Test Product", price=100.00, warehouse_quantity=50, vendor=self.vendor
        )
        self.product_url = reverse('vendorproduct-detail', args=[self.product.id])

    def test_vendor_can_view_own_product_details(self):
        """Ensure vendors can view their own product details."""
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_can_add_and_update_own_product(self):
        """Ensure vendors can add and update their own products."""
        url = reverse('vendorproduct-list')
        data = {
            "name": "New Product",
            "price": 200.00,
            "warehouse_quantity": 30,
            "vendor": self.vendor.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data['id']

        update_url = reverse('vendorproduct-detail', args=[product_id])
        update_data = {"warehouse_quantity": 60}
        response = self.client.patch(update_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_cannot_modify_other_vendors_product(self):
        """Ensure vendors cannot modify products from other vendors."""
        other_vendor = Vendor.objects.create(name="Other Vendor")
        other_product = VendorProduct.objects.create(
            name="Other Product", price=100.00, warehouse_quantity=50, vendor=other_vendor
        )
        url = reverse('vendorproduct-detail', args=[other_product.id])
        data = {"warehouse_quantity": 30}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
