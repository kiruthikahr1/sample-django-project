# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from .models import Order, OrderStatus, Payment

BASE_URL = 'http://localhost:8000'


def get_order_by_id(order_id):
    try:
        order = Order.objects.get(id=order_id)
        return order
    except Order.DoesNotExist:
        return None


def create_example_order(status=OrderStatus.NEW, amount=100):
    return Order.objects.create(
        delivery_name="John Doe",
        delivery_address="123, Main st, State",
        amount=amount,
        status=status,
    )


def payment_exists_for_order(order_id):
    return True if Payment.objects.filter(order__id=order_id) else False


def create_payment_for_order(order):
    payment = Payment(order=order, amount=order.amount)
    payment.save()
    return payment


class OrderView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_template = BASE_URL + '/orders/{}/'

    def test_view_with_existing_order(self):
        order = create_example_order()
        url = self.url_template.format(order.id)
        res = self.client.get(url)
        self.assertTemplateUsed(res, 'orders/order_details.html')
        self.assertContains(res, order.id, status_code=200)
        self.assertContains(res, order.delivery_name, status_code=200)
        self.assertContains(res, order.delivery_address, status_code=200)
        self.assertContains(res, order.amount, status_code=200)
        self.assertContains(res, order.status, status_code=200)

    def test_view_with_non_existing_order(self):
        order_id = 10
        self.assertIsNone(get_order_by_id(order_id))

        url = self.url_template.format(order_id)
        res = self.client.get(url)
        self.assertTemplateUsed(res, 'errors/404.html')
        self.assertContains(res, "Object you are trying to access does not exist", status_code=200)


class DispatchOrder(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_template = BASE_URL + '/orders/{}/dispatch/'

    def test_dispatch_with_new_order(self):
        order = create_example_order(status=OrderStatus.NEW)
        url = self.url_template.format(order.id)
        res = self.client.post(url)

        self.assertRedirects(res, '/orders/')

    def test_dispatch_with_dispatched_order(self):
        order = create_example_order(status=OrderStatus.DISPATCHED)
        url = self.url_template.format(order.id)
        res = self.client.post(url)

        self.assertTemplateUsed(res, 'errors/400.html')
        self.assertContains(res, "Only new orders can be dispatched")

    def test_dispatch_with_delivered_order(self):
        order = create_example_order(status=OrderStatus.DELIVERED)
        url = self.url_template.format(order.id)
        res = self.client.post(url)

        self.assertTemplateUsed(res, 'errors/400.html')
        self.assertContains(res, "Only new orders can be dispatched")

    def test_dispatch_with_non_existing_order(self):
        order_id = 10
        self.assertIsNone(get_order_by_id(order_id))

        url = self.url_template.format(order_id)
        res = self.client.post(url)
        self.assertTemplateUsed(res, 'errors/404.html')
        self.assertContains(res, "Object you are trying to access does not exist", status_code=200)


class PayOrder(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_template = BASE_URL + '/orders/{}/payments/'

    def test_pay_with_dispatched_order(self):
        order = create_example_order(status=OrderStatus.DISPATCHED)
        url = self.url_template.format(order.id)
        payload = {'amount': order.amount}
        res = self.client.post(url, payload)

        self.assertRedirects(res, '/orders/')

    def test_pay_with_dispatched_order_and_non_integer_amount(self):
        order = create_example_order(status=OrderStatus.DISPATCHED)
        url = self.url_template.format(order.id)
        payload = {'amount': '123foo'}
        res = self.client.post(url, payload)

        self.assertTemplateUsed(res, 'errors/5xx.html')
        self.assertContains(res, "Server error")

    def test_pay_with_dispatched_order_and_not_matching_amount(self):
        order = create_example_order(status=OrderStatus.DISPATCHED, amount=100)
        url = self.url_template.format(order.id)
        payload = {'amount': 99}
        res = self.client.post(url, payload)

        self.assertTemplateUsed(res, 'errors/400.html')
        self.assertContains(res, "Order value and payment amount does not match")

    def test_pay_with_dispatched_and_already_paid_order(self):
        order = create_example_order(status=OrderStatus.DISPATCHED, amount=100)
        create_payment_for_order(order)
        self.assertTrue(payment_exists_for_order(order.id))

        url = self.url_template.format(order.id)
        payload = {'amount': order.amount}
        res = self.client.post(url, payload)

        self.assertTemplateUsed(res, 'errors/400.html')
        self.assertContains(res, "Order already has a payment attached")

    def test_pay_with_new_order(self):
        order = create_example_order(status=OrderStatus.NEW)

        url = self.url_template.format(order.id)
        payload = {'amount': order.amount}
        res = self.client.post(url, payload)

        self.assertTemplateUsed(res, 'errors/400.html')
        self.assertContains(res, "Only dispatched orders can be paid")

    def test_pay_with_delivered_order(self):
        order = create_example_order(status=OrderStatus.DELIVERED)

        url = self.url_template.format(order.id)
        payload = {'amount': order.amount}
        res = self.client.post(url, payload)

        self.assertTemplateUsed(res, 'errors/400.html')
        self.assertContains(res, "Only dispatched orders can be paid")

    def test_pay_with_non_existing_order(self):
        order_id = 10
        self.assertIsNone(get_order_by_id(order_id))

        url = self.url_template.format(order_id)
        res = self.client.post(url)

        self.assertContains(res, "Object you are trying to access does not exist", status_code=200)
