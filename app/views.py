from django.views.generic import ListView, DetailView
from django.views import View
from .services import save_order, dispatch_order, get_order_by_id, process_payment
from .models import Order, Payment
from django.shortcuts import render, redirect


class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"


class OrderDetailView(View):
    template_name = "orders/order_details.html"

    def get(self, request, pk, format=None):
        order = get_order_by_id(pk)
        return render(request, 'orders/order_details.html', {"order": order})


class OrderDispatchView(View):
    def post(self, request, order_id, format=None):
        order = get_order_by_id(order_id)
        dispatch_order(order)
        return redirect("/orders/")


class OrderPaymentView(View):
    def post(self, request, order_id, format=None):
        order = get_order_by_id(order_id)
        amount = int(request.POST.get("amount"))
        process_payment(order, amount)

        return redirect("/orders/")
