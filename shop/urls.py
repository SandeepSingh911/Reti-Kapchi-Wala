
from django.urls import path
from django.urls.base import reverse_lazy
from shop import views
from django.contrib.auth import views as auth_views

app_name = "myapp"

urlpatterns = [

    # -----pages url ----
    path('', views.index, name="index"),

    path('about/', views.about, name="about"),

    path('shop/', views.shop, name="shop"),
    path('shop/<slug:filter>', views.shop, name="product_filter"),

    path('add_to_cart/', views.AddToCart, name="add_to_cart"),

    path('cart/', views.cart, name="cart"),

    path('pluscart/', views.plus_cart, name="plus_cart"),
    path('minuscart/', views.minus_cart, name="minus_cart"),
    path('removecart/', views.remove_cart, name="remove_cart"),

    path('checkout/', views.checkout, name="checkout"),

    path('paymentdone/', views.payment, name="paymentdone"),

    path('add_to_wishlist/', views.AddTowishlist, name="add_to_wishlist"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('removewishlist/', views.remove_wishlist, name="remove_wishlist"),

    path('profile/', views.profile, name="profile"),

    path('myorders/', views.orders, name="myorders"),

    # path('contact/', views.contact, name="contact"),

    path('register/', views.registraion, name="registratiion"),

    path('login/', views.login, name="login"),

    path('logout/', views.logout, name="logout"),
    # -----pages url end----

    # ----filter products link------
    path('cement/', views.filterBycement, name="cement"),
    path('structural_steel/', views.filterBystructuralsteel,
         name="structural_steel"),
    path('reinforcement_steel/', views.filterByreinforcementsteel,
         name="reinforcement_steel"),
    path('bitumen/', views.filterBybitumen, name="bitumen"),

    path('Price0to500/', views.filterByPrice0to500,
         name="Price0to500"),
    path('Price500to1000/', views.filterByPrice500to1000,
         name="Price500to1000"),
    path('Price1000to5000/', views.filterByPrice1000to5000,
         name="Price1000to5000"),
    path('Price5000to10000/', views.filterByPrice5000to10000,
         name="Price5000to10000"),
    # ----search-----
    path('search/', views.search, name="search"),

    # ------password change url-----

    path('password_change/complete/', auth_views.PasswordChangeDoneView.as_view(
         template_name='registration/password_change_done.html'), name="password_change_done"),

    # path('password_change/done/abc', views.passwordchanged,name="password_changed"),

    path('password_change/', auth_views.PasswordChangeView.as_view(
         success_url=reverse_lazy('myapp:password_change_done'), template_name='registration/password_change.html'), name="password_change"),

    path('password_reset/done', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_done.html'), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='registration/password_reset.html',
         success_url=reverse_lazy('myapp:password_reset_complete'),),
         name="password_reset_confirm"),

    path('password_reset/', auth_views.PasswordResetView.as_view(

         email_template_name='registration/password_reset_email.html',
         success_url=reverse_lazy('myapp:password_reset_done'),), name="password_reset"),

    path('reset/done', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name="password_reset_complete"),

    # ------password change url end-----
    # -----Address update and delete urls----
    path('address/update<int:pk>',
         views.UpdateAddressView.as_view(), name="address_update"),
    path('address/delete<int:pk>',
         views.DeleteAddressView.as_view(), name="address_delete"),
    # -----//Address update and delete urls----








    path('product/add', views.addProduct.as_view(), name="add_product"),

    path('product/list', views.listProduct.as_view(), name="list_product"),

    path('details/product<int:pk>',
         views.detailProduct.as_view(), name="detail_product"),

    path('product/update<int:pk>',
         views.updateProduct.as_view(), name="update_product"),

    path('product/delete<int:pk>',
         views.deleteProduct.as_view(), name="delete_product"),

    # catorg

    path('add/catorgie', views.addCategorie.as_view(), name="add_categorie"),

    path('list/catorgie', views.listCategorie.as_view(), name="list_categorie"),

    path('details/catorgie<int:pk>', views.detailCategorie.as_view(),
         name="details_categorie"),

    path('delete/catorgie<int:pk>',
         views.deleteCategorie.as_view(), name="delete_categorie"),

    # ------------0rders---------------------

    path('orders/update<int:pk>',
         views.updateOrder.as_view(), name="order_update"),

    path('orders', views.manageOrders, name="order_list"),
]
