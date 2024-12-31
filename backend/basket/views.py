from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Basket
from .serializers import BasketSerializer


class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Получение корзины текущего пользователя"""
        basket = Basket.objects.filter(user=request.user)
        serializer = BasketSerializer(basket, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Добавление товара в корзину"""
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = BasketSerializer(data=data)
        if serializer.is_valid():
            basket_item, created = Basket.objects.get_or_create(
                user=request.user,
                product_id=data["product"],
                defaults={"quantity": data.get("quantity", 1)},
            )
            if not created:
                basket_item.quantity += data.get("quantity", 1)
                basket_item.save()

            return Response(
                BasketSerializer(basket_item).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Удаление товара из корзины"""
        try:
            basket_item = Basket.objects.get(user=request.user, pk=pk)
            basket_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Basket.DoesNotExist:
            return Response(
                {"error": "Item not found in your basket"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request, pk):
        """Обновление количества товара в корзине"""
        try:
            basket_item = Basket.objects.get(user=request.user, pk=pk)
            new_quantity = request.data.get("quantity")
            if new_quantity is not None and int(new_quantity) > 0:
                basket_item.quantity = int(new_quantity)
                basket_item.save()
                return Response(
                    BasketSerializer(basket_item).data, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Basket.DoesNotExist:
            return Response(
                {"error": "Item not found in your basket"},
                status=status.HTTP_404_NOT_FOUND,
            )
