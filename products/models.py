from django.db import models
from django.urls import reverse
import uuid


# Category model to categorize products
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

    def first_image(self):
        all_media = self.media.all()
        # images = [media for media in all_media if media.type == ProductMedia.image]
        print(str(all_media[0]))
        return all_media[0] if all_media else None


class ProductMedia(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="media",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="products", blank=True, null=True)
    alt = models.CharField(max_length=250, blank=True)
    external_url = models.CharField(max_length=256, blank=True, null=True)
