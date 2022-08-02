from django.db       import models

from users.models    import User
from products.models import ProductOption

class Cart(models.Model) :
    user           = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity       = models.IntegerField(default=0)
    
    class Meta :
        db_table = 'carts'