from .models import Order, OrderStatus, Payment
from .exceptions import InvalidDataException, ServiceException, ObjectNotFoundException


def get_order_by_id(order_id: int) -> Order:
    try:
        order = Order.objects.get(id=order_id)
        return order
    except Order.DoesNotExist:
        raise ObjectNotFoundException("Invalid order object")
    except Exception as e:
        raise ServiceException("Error in retrieving order object")


def save_order(order: Order):
    order.status = OrderStatus.NEW
    order.save()


def dispatch_order(order: Order):
    if order.status != OrderStatus.NEW.name:
        # problem: throw error here
        raise InvalidDataException("Only new orders can be dispatched")

    order.status = OrderStatus.DISPATCHED
    order.save()


def process_payment(order: Order, amount):
    # only orders in Dispatched status can be delivered
    if order.status != OrderStatus.DISPATCHED.name:
        # problem: throw error here
        raise InvalidDataException("Only dispatched orders can be paid")

    # order amount and payment amount must tally
    if order.amount != amount:
        # problem: throw error here
        raise InvalidDataException("Order value and payment amount does not match")

    already_paid = Payment.objects.filter(order__id=order.id)

    if already_paid:
        raise InvalidDataException("Order already has a payment attached")

    payment = Payment(order=order, amount=amount)
    payment.save()
    order.payment = payment
    order.status = OrderStatus.DELIVERED
    order.save()

    return payment
