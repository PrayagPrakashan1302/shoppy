from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('product/<int:product_id>/', views.productdetail, name="productdetail"),
    path('remove_items/', views.removeUserCartItems, name='remove_items'),
 
   
]
