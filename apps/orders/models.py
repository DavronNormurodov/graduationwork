from django.db.models import Model,\
                             CharField,\
                             TextField, \
                             IntegerField,\
                             FloatField,\
                             JSONField,\
                             DateField,\
                             ForeignKey,\
                             CASCADE,\
                             SET_NULL

from users.models import User
from products.models import Product

status_choice = (
    ('active', 'Active'),
    ('process', 'Process'),
    ('cancelled', 'Cancelled'),
    ('delivered', 'Delivered')
)


class Order(Model):
    user = ForeignKey('users.User', CASCADE, 'user')
    total_price = FloatField(default=0)
    location = JSONField(null=True)
    description = TextField(null=True)
    status = CharField(max_length=10, choices=status_choice, default='active')
    shipping_type = CharField(max_length=100, null=True, blank=True, default='fast')
    address = CharField(max_length=255, null=True, blank=True)
    broker = CharField(max_length=100, null=True, blank=True)
    created_at = DateField(auto_now_add=True)

    def order_info(self):
        return self.__dict__

    def __str__(self):
        return f"#[{self.id}] {self.user.name}"


class OrderProduct(Model):
    order = ForeignKey(Order, CASCADE, 'products')
    product = ForeignKey(Product, SET_NULL, null=True)
    amount = IntegerField(default=0)
