import glob
from os import path
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Vendor, VendorProduct
from products.models import Product, ProductMedia
from faker import Faker
import uuid
from definitions import ROOT_DIR

fake = Faker()
User = get_user_model()

vendors_detail_url = "vendors-detail"
vendors_list_url = "vendors-list"
vendors_product_list_url = "vendor-products-list"
vendors_product_detail_url = "vendor-products-detail"
rating_list_url = "vendor-ratings-list"
rating_detail_url = "vendor-ratings-detail"


class VendorProductViewSetTestCase(APITestCase):
    """Test case for VendorProduct viewsets"""

    def get_image_list(self):
        images_list = glob.glob(
            path.join(ROOT_DIR, "static\\img\\saloerphotos\\saloerplaceholders\\*.png")
        )
        images_list = [x[len(ROOT_DIR) :] for x in images_list]
        return images_list

    def setUp(self):
        """Set up necessary users, vendors, products, and vendor products"""
        self.user = User.objects.create_user(username="vendoruser", password="password")
        self.vendor = Vendor.objects.create(
            owner=self.user,
            store_name=fake.company(),
            store_address=fake.address(),
            store_bio=fake.text(),
            contact_number=fake.phone_number(),
        )
        self.product = Product.objects.create(name="Test Product")
        self.vendor_product = VendorProduct.objects.create(
            vendor=self.vendor,
            product=self.product,
            price=10.00,
            warehouse_quantity=100,
        )
        selected_images = fake.random_elements(
            elements=self.get_image_list(),
            length=fake.random_int(min=1, max=5),
            unique=True,
        )
        for i in selected_images:
            ProductMedia.objects.create(
                product=self.product,
                image=i,
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_vendor_products(self):
        """Test that we can list all vendor products"""
        response = self.client.get(
            reverse(vendors_product_list_url, kwargs={"vendor_pk": self.vendor.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_by_vendor(self):
        """Test filtering vendor products by vendor ID"""
        response = self.client.get(
            reverse(
                vendors_product_list_url,
                kwargs={"vendor_pk": self.vendor.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_product(self):
        """Test filtering vendor products by product ID"""
        response = self.client.get(
            reverse(
                vendors_product_detail_url,
                kwargs={"vendor_pk": self.vendor.id, "pk": self.vendor_product.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_vendor_product(self):
        """Test retrieving a single vendor product by ID"""
        response = self.client.get(
            reverse(
                vendors_product_detail_url,
                kwargs={"vendor_pk": self.vendor.id, "pk": self.vendor_product.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], "10.00")

    def test_create_vendor_product(self):
        """Test creating a vendor product."""
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "20.00",
            "warehouse_quantity": 50,
        }
        response = self.client.post(
            reverse(
                vendors_product_detail_url,
                kwargs={"vendor_pk": self.vendor.id, "pk": self.vendor_product.id},
            ),
            payload,
        )
        print(response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorProduct.objects.count(), 2)
        self.assertEqual(VendorProduct.objects.latest("id").price, 20.00)

    # Add test for vendor product creation with invalid data (missing fields)
    def test_create_vendor_product_invalid_data(self):
        """Test creating a vendor product with invalid data fails"""
        payload = {
            # "vendor": None,  # Missing required field
            "product": self.product.id,
            "price": "20.00",
            "warehouse_quantity": 50,
        }
        response = self.client.post(
            reverse(vendors_product_list_url, kwargs={"vendor_pk": self.vendor.id}),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_vendor_product(self):
        """Test updating a vendor product"""
        payload = {"price": "15.00"}
        response = self.client.patch(
            reverse(
                vendors_product_detail_url,
                kwargs={"vendor_pk": self.vendor.id, "pk": self.vendor_product.id},
            ),
            payload,
        )
        self.vendor_product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.vendor_product.price, 15.00)

    def test_delete_vendor_product(self):
        """Test deleting a vendor product"""
        response = self.client.delete(
            reverse(
                vendors_product_detail_url,
                kwargs={"vendor_pk": self.vendor.id, "pk": self.vendor_product.id},
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VendorProduct.objects.count(), 0)

    # Add test for filtering by non-existent vendor/product ID
    def test_filter_by_nonexistent_vendor(self):
        """Test filtering by non-existent vendor ID returns empty result"""
        response = self.client.get(
            reverse(
                vendors_product_list_url,
                kwargs={"vendor_pk": self.vendor.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_by_nonexistent_product(self):
        """Test filtering by non-existent product ID returns empty result"""
        response = self.client.get(
            reverse(
                vendors_detail_url,
                kwargs={"pk": "111111"},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
