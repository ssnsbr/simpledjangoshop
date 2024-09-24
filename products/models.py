from django.db import models
from django.urls import reverse
import uuid
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.text import slugify


# Category model to categorize products
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def available_products():
        return Product.objects.filter(vendor_products__available=True).distinct()

    @staticmethod
    def filter_by_price(min_price, max_price):
        return Product.objects.filter(
            vendor_products__price__gte=min_price, vendor_products__price__lte=max_price
        ).distinct()

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(self.name+self.id)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

    def first_image(self):
        all_media = self.media.all()
        # images = [media for media in all_media if media.type == ProductMedia.image]
        print(str(all_media[0]))
        return all_media[0] if all_media else None  #'/static/img/default_product.png'


def validate_image(image):
    try:
        img = Image.open(image)
        img.verify()
    except Exception:
        raise ValidationError("Uploaded file is not a valid image.")


class ProductMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        related_name="media",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to="products", validators=[validate_image], blank=True, null=True
    )
    alt = models.CharField(max_length=250, blank=True)
    external_url = models.CharField(max_length=256, blank=True, null=True)
