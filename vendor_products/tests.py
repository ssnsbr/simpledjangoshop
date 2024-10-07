import glob
from os import path
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Product, ProductMedia
from faker import Faker
import uuid
from definitions import ROOT_DIR
from tests.utils import query_reverse
from vendor_products.models import VendorProduct
from vendors.models import Vendor
from decimal import Decimal

fake = Faker()
User = get_user_model()

vendors_product_list_url = "vendor-products-list"
vendors_product_detail_url = "vendor-products-detail"


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
            reverse(vendors_product_list_url, args={"v": self.vendor.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_by_vendor(self):
        """Test filtering vendor products by vendor ID"""
        response = self.client.get(
            reverse(
                vendors_product_list_url,
                args={"v": self.vendor.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_product(self):
        """Test filtering vendor products by product ID"""
        response = self.client.get(
            reverse(
                vendors_product_detail_url,
                args={"p": self.vendor_product.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_vendor_product(self):
        """Test retrieving a single vendor product by ID"""
        print("1:",query_reverse(
                vendors_product_detail_url,
                kwargs={"pk": self.vendor_product.id},
            ))
        print("2:",query_reverse(
                vendors_product_list_url,
                query={"v": self.vendor.id},
            ))
        response = self.client.get(
            query_reverse(
                vendors_product_detail_url,
                kwargs={"pk": self.vendor_product.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
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
                kwargs={"pk": self.vendor_product.id},
            ),
            payload,
        )
        # print(response.content, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,  "response:" + str(response.content),)
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
            reverse(vendors_product_list_url, args={"v": self.vendor.id}),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),)

    def test_update_vendor_product(self):
        """Test updating a vendor product"""
        payload = {"price": "15.00"}
        response = self.client.patch(
            reverse(
                vendors_product_detail_url,
                kwargs={"pk": self.vendor_product.id},
            ),
            payload,
        )
        self.vendor_product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(self.vendor_product.price, 15.00)

    def test_delete_vendor_product(self):
        """Test deleting a vendor product"""
        response = self.client.delete(
            reverse(
                vendors_product_detail_url,
                kwargs={"pk": self.vendor_product.id},
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
                args={"v": self.vendor.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(len(response.data), 0)

    def test_filter_by_nonexistent_product(self):
        """Test filtering by non-existent product ID returns empty result"""
        response = self.client.get(
            reverse(
                vendors_product_detail_url,
                kwargs={"pk": str(uuid.uuid4())},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(len(response.data), 0)


class VendorProductViewSetTestCase2(APITestCase):
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
        """Test listing all vendor products"""
        response = self.client.get(
            reverse(vendors_product_list_url, args={"v": self.vendor.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_vendor_product(self):
        """Test retrieving a single vendor product by ID"""
        response = self.client.get(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(response.data["price"], "10.00")

    def test_create_vendor_product(self):
        """Test creating a vendor product with valid data"""
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "20.00",
            "warehouse_quantity": 50,
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,  "response:" + str(response.content),
            "response:" + str(response.content),
        )
        
        self.assertEqual(VendorProduct.objects.count(), 2)
        self.assertEqual(VendorProduct.objects.latest("id").price, 20.00)

    def test_create_vendor_product_invalid_data(self):
        """Test creating a vendor product with missing or invalid fields"""
        payload = {
            "product": self.product.id,
            "price": "20.00",
            "warehouse_quantity": 50,
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),)

        # Edge case: Create product with zero price or quantity
        invalid_payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "0.00",  # Zero price
            "warehouse_quantity": 0,  # Zero stock
        }
        response = self.client.post(reverse(vendors_product_list_url), invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),
            "response:" + str(response.content),)

    def test_update_vendor_product(self):
        """Test updating a vendor product"""
        payload = {"price": 15.00}
        response = self.client.patch(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id}),
            payload,
        )
        self.vendor_product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            "response:" + str(response.content),)
        self.assertEqual(self.vendor_product.price, 15.00)

    def test_update_vendor_product_invalid_data(self):
        """Test updating a vendor product with invalid data"""
        payload = {"price": "-15.00"}  # Negative price
        response = self.client.patch(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id}),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  
            "response:" + str(response.content),)

    def test_delete_vendor_product(self):
        """Test deleting a vendor product"""
        response = self.client.delete(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            "response:" + str(response.content),)
        self.assertEqual(VendorProduct.objects.count(), 0)

    def test_filter_by_nonexistent_vendor(self):
        """Test filtering by non-existent vendor ID returns empty result"""
        response = self.client.get(
            reverse(
                vendors_product_list_url, args={"v": str(uuid.uuid4()).replace("-", "")}
            )
        )
        self.assertEqual(response.content.decode(), '{"detail":"Not found."}', "response:" + str(response.content),)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, "response:" + str(response.content),)
        self.assertEqual(len(response.data), 0,"response:" + str(response.data))

    def test_filter_by_nonexistent_product(self):
        """Test filtering by non-existent product ID returns empty result"""
        response = self.client.get(
            reverse(vendors_product_detail_url, args={"p": str(uuid.uuid4())}).replace(
                "-", ""
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            "response:" + str(response.content),)
        self.assertEqual(len(response.data), 0)

    def test_by_wrong_uuid_format(self):
        """Test filtering by wrong UUID format"""
        response = self.client.get(
            reverse(vendors_product_detail_url, args={"p": "11"})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            "response:" + str(response.content),)
        self.assertEqual(len(response.data), 0)

    def test_delete_nonexistent_vendor_product(self):
        """Test trying to delete a non-existent vendor product"""
        response = self.client.delete(
            reverse(
                vendors_product_detail_url,
                kwargs={"pk": str(uuid.uuid4()).replace("-", "")},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Add tests for more edge cases: zero price, large quantities, etc.


class VendorProductViewSetEdgeCaseTestCase(APITestCase):
    """Test case for VendorProduct viewsets handling edge cases"""

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
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_vendor_product_with_zero_price(self):
        """Test creating a vendor product with a zero price fails"""
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "0.00",  # Zero price
            "warehouse_quantity": 50,
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),)
        self.assertIn("price", response.data)
        self.assertIn(
            "Ensure this value is greater than or equal to 0.01", response.data["price"]
        )

    def test_create_vendor_product_with_negative_price(self):
        """Test creating a vendor product with a negative price fails"""
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "-10.00",  # Negative price
            "warehouse_quantity": 50,
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),)
        self.assertIn("price", response.data)
        self.assertIn(
            "Ensure this value is greater than or equal to 0.01", response.data["price"]
        )

    def test_create_vendor_product_with_negative_quantity(self):
        """Test creating a vendor product with a negative warehouse quantity fails"""
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "20.00",
            "warehouse_quantity": -10,  # Negative stock
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),)
        self.assertIn("warehouse_quantity", response.data)
        self.assertIn(
            "Ensure this value is greater than or equal to 0",
            response.data["warehouse_quantity"],
        )

    def test_create_vendor_product_with_large_quantity(self):
        """Test creating a vendor product with a very large quantity succeeds"""
        large_quantity = 10**9  # 1 billion items in stock
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "50.00",
            "warehouse_quantity": large_quantity,  # Large stock quantity
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,  "response:" + str(response.content),)
        self.assertEqual(
            VendorProduct.objects.latest("id").warehouse_quantity, large_quantity
        )

    def test_update_vendor_product_with_zero_price(self):
        """Test updating a vendor product with zero price fails"""
        payload = {"price": "0.00"}  # Zero price
        response = self.client.patch(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id}),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),)
        self.assertIn("price", response.data)
        self.assertIn(
            "Ensure this value is greater than or equal to 0.01", response.data["price"]
        )

    def test_update_vendor_product_with_negative_quantity(self):
        """Test updating a vendor product with negative warehouse quantity fails"""
        payload = {"warehouse_quantity": -100}  # Negative stock
        response = self.client.patch(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id}),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,  "response:" + str(response.content),)
        self.assertIn("warehouse_quantity", response.data)
        self.assertIn(
            "Ensure this value is greater than or equal to 0",
            response.data["warehouse_quantity"],
        )

    def test_update_vendor_product_with_large_quantity(self):
        """Test updating a vendor product with very large quantity succeeds"""
        large_quantity = 10**9  # 1 billion items in stock
        payload = {"warehouse_quantity": large_quantity}
        response = self.client.patch(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id}),
            payload,
        )
        self.vendor_product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(self.vendor_product.warehouse_quantity, large_quantity)

    def test_create_vendor_product_with_smallest_valid_price(self):
        """Test creating a vendor product with the smallest valid price succeeds"""
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": "0.01",  # Smallest valid price
            "warehouse_quantity": 50,
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,  "response:" + str(response.content),)
        self.assertEqual(VendorProduct.objects.latest("id").price, Decimal("0.01"))

    def test_create_vendor_product_with_maximum_price(self):
        """Test creating a vendor product with a very large price succeeds"""
        large_price = 10**6  # 1 million
        payload = {
            "vendor": self.vendor.id,
            "product": self.product.id,
            "price": large_price,
            "warehouse_quantity": 50,
        }
        response = self.client.post(reverse(vendors_product_list_url), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,  "response:" + str(response.content),)
        self.assertEqual(VendorProduct.objects.latest("id").price, Decimal(large_price))

    def test_update_vendor_product_with_maximum_price(self):
        """Test updating a vendor product with a very large price succeeds"""
        large_price = 10**6  # 1 million
        payload = {"price": large_price}
        response = self.client.patch(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id}),
            payload,
        )
        self.vendor_product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(self.vendor_product.price, Decimal(large_price))

    def test_update_vendor_product_with_smallest_valid_price(self):
        """Test updating a vendor product with the smallest valid price succeeds"""
        payload = {"price": "0.01"}  # Smallest valid price
        response = self.client.patch(
            reverse(vendors_product_detail_url, kwargs={"pk": self.vendor_product.id}),
            payload,
        )
        self.vendor_product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK,  "response:" + str(response.content),)
        self.assertEqual(self.vendor_product.price, Decimal("0.01"))
