# -*- coding: utf-8 -*-

from django.db import models
import enum


class OrderStatus(enum.Enum):
    NEW = "New"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"

    def __str__(self):
        return self.name


class Order(models.Model):
    delivery_name = models.CharField(max_length=200)
    delivery_address = models.TextField()
    amount = models.FloatField()
    status = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in OrderStatus],
        blank=True,
        null=True,
        default=OrderStatus.NEW
    )
    created_date = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
