from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartItemSerializer


class CartListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return cart.items.all()

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            cart, created = Cart.objects.get_or_create(user=user)
            serializer.save(cart=cart)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
