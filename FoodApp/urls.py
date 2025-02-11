from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('categories/',views.categories,name='categories'),
    path('categories_view/<str:slug>',views.categoryview,name='categoryview'),
    path('categories_view/<str:catslug>/<str:prodslug>/',views.productview,name='productview'),
    path('add-to-cart/',views.addTocart,name='addTocart'),
    path('cart/',views.cartview,name='cartview'),
    path('updatecart/',views.updatecartqty,name='updatecart'),
    path('deletecart/',views.deletecart,name='deletecart'),
    path('add_w_list/',views.add_w_list,name='add_w_list'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_wish/',views.removewish,name='remove_wish'),
    path('checkout/',views.checkout,name='checkout'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('get_amount/',views.get_amount,name='amount'),
    path('my-orders/',views.orderss,name='orders'),
    path('searchproducts/',views.search),
    path('searchitems/',views.searchproducts,name="searchproduct"),
    path('orders/',views.orders,name="orders"),
    path('orders/<int:order_id>/',views.order_detail, name='order_detail'),
    path('about',views.aboutus, name='about'),
]
