from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer, Product, Order, OrderItem
from .serializers import (
    CustomerSerializer,
    ProductSerializer,
    OrderReadSerializer,
    OrderCreateSerializer,
    OrderItemCreateSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("-id")
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = (
        Order.objects
        .select_related("customer")
        .prefetch_related("items__product")
        .order_by("-id")
    )

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderReadSerializer


    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.validated_data

        customer = Customer.objects.get(id=data["customer_id"])

        order = Order.objects.create(customer=customer)

        for item in data.get("items", []):
            product = Product.objects.get(id=item["product_id"])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                unit_price=product.price
            )

        serializer.instance = order


    @action(detail=True, methods=["post"], url_path="items")
    @transaction.atomic
    def add_item(self, request, pk=None):

        order = self.get_object()

        ser = OrderItemCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        product = Product.objects.get(id=ser.validated_data["product_id"])
        quantity = ser.validated_data["quantity"]

        item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                "quantity": quantity,
                "unit_price": product.price
            }
        )

        if not created:
            item.quantity += quantity
            item.save()

        order.refresh_from_db()

        return Response(OrderReadSerializer(order).data)