# Generated by Django 5.0.7 on 2024-10-01 06:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_productattribute_producttype_and_more'),
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('warehouse_quantity', models.PositiveIntegerField()),
                ('available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='vendors.vendordiscount')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='vendors.vendor')),
            ],
            options={
                'indexes': [models.Index(fields=['vendor', 'product'], name='vendor_prod_vendor__8a697a_idx'), models.Index(fields=['available'], name='vendor_prod_availab_844084_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='vendorproduct',
            constraint=models.UniqueConstraint(fields=('vendor', 'product'), name='vendor product constraint'),
        ),
    ]
