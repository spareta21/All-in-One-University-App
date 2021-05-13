from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index.html'),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("canteen", views.canteen, name="canteen"),
    path("cleanliness", views.cleanliness, name="cleanliness"),
    path("logout", views.logout, name="logout"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("orders", views.orders, name="orders"),
    path("cleanliness", views.cleanliness, name="cleanliness"),
    path("cleanliness_admin", views.cleanliness_admin, name="cleanliness_admin"),
    path("canteen_admin", views.canteen_admin, name="canteen_admin"),
    path("view_order", views.view_order, name="view_order"),
    path("view_complaints", views.view_complaints, name="view_complaints")
]