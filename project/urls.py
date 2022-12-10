from django.urls import path
from app.views import *

urlpatterns = [
    path("orders/", OrderListView.as_view()),
    path("orders/<pk>/", OrderDetailView.as_view()),
    path("orders/<order_id>/dispatch/", OrderDispatchView.as_view()),
    path("orders/<order_id>/payments/", OrderPaymentView.as_view()),
]
