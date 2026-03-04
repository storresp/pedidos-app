from django.db import models
from django.db.models import Sum

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Customer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Product(models.Model):
    name = models.CharField(max_length=160)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="orders")

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)

    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        unique_together = [("order", "product")]  # evita duplicar el mismo producto en un pedido

    def save(self, *args, **kwargs):

        # llenar precio unitario automáticamente desde el producto
        if not self.unit_price:
            self.unit_price = self.product.price

        # calcular total de la linea
        self.line_total = self.unit_price * self.quantity

        super().save(*args, **kwargs)

        # recalcular total del pedido
        total = self.order.items.aggregate(
            Sum("line_total")
        )["line_total__sum"] or 0

        self.order.total = total
        self.order.save(update_fields=["total"])


    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order_id})"


    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)

        total = order.items.aggregate(Sum("line_total"))["line_total__sum"] or 0
        order.total = total
        order.save(update_fields=["total"])
