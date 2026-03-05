from django.db import transaction
from rest_framework import viewsets, status
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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Buscar o crear el customer por correo
        customer, _ = Customer.objects.get_or_create(
            email=data["correo"],
            defaults={"name": data["nombre"]}
        )
        # Si ya existía, actualizar el nombre por si cambió
        if customer.name != data["nombre"]:
            customer.name = data["nombre"]
            customer.save(update_fields=["name"])

        order = Order.objects.create(customer=customer)

        for item in data.get("items", []):
            try:
                product = Product.objects.get(id=item["product_id"])
            except Product.DoesNotExist:
                return Response(
                    {"detail": f"Producto con ID {item['product_id']} no encontrado."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.get("quantity", 1),
                unit_price=product.price
            )

        read_serializer = OrderReadSerializer(order)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

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