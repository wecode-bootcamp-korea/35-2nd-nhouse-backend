from django.db       import models

from core.models     import TimeStampModel
from users.models    import User
from products.models import ProductOption
    
class Order(TimeStampModel) :
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status      = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    sender            = models.CharField(max_length=50)
    recipient         = models.CharField(max_length=50)
    recipient_contact = models.CharField(max_length=200)
    address           = models.TextField()

    class Meta :
       db_table = 'orders'

class OrderStatus(models.Model) :
    name = models.CharField(max_length=200)

    class Meta :
       db_table = 'orders_status'

class OrderItem(models.Model) :
    order              = models.ForeignKey('Order', on_delete=models.CASCADE)
    option             = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity           = models.IntegerField()
    order_items_status = models.ForeignKey('OrderItemStatus', on_delete=models.CASCADE)

    class Meta :
       db_table = 'order_items'

class OrderItemStatus(models.Model) :
    name = models.CharField(max_length=200)

    class Meta :
       db_table = 'order_items_status'