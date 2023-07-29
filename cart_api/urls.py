from django.urls import path
from .views import CartItemListView, CartDetailView, CartItemDeleteView

urlpatterns = [
    path('items', CartItemListView.as_view(), name='cart-list-create'),
    path('detail', CartDetailView.as_view(), name='cart-detail-create'),
    path('items/delete/<int:pk>/', CartItemDeleteView.as_view(),
         name='cart-item-delete'),
]
