from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartDetailSerializer
from rest_framework import status, permissions


class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    # i had to this, otherwise it was not iterable
    # get_queryset name is not optional
    def get_queryset(self):
        try:
            user = self.request.user
            cart, created = Cart.objects.get_or_create(user=user)
            return cart.items.all()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                cart, created = Cart.objects.get_or_create(user=user)
                serializer.save(cart=cart)
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartDetailSerializer
    permission_classes = [IsAuthenticated]

    # get_object name is not optional
    def get_object(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            cart_item = self.get_object()
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
