from django.urls import path
from .views import initiate_payment, callback

urlpatterns = [
    path('checkout/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
]
