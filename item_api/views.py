from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
import os


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser


class ItemView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]

    def get(self, request):
        try:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class SingleItemView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]

    def get(self, request, slug):
        try:
            item = Item.objects.get(slug=slug)
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        try:
            item = Item.objects.get(slug=slug)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        try:
            item = Item.objects.get(slug=slug)
            # Check if the product_image field contains a file
            if item.product_image:
                file_path = item.product_image.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            item.delete()
            return Response("Item Deleted", status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
