from django.db       import models

from core.models     import TimeStampModel
from users.models    import User
from products.models import Product

class Post(TimeStampModel):
    title       = models.CharField(max_length=45)
    content     = models.TextField()
    cover_image = models.URLField(max_length=300)
    living_type = models.CharField(max_length=45)
    room_size   = models.CharField(max_length=45)
    family_type = models.CharField(max_length=45)
    work_type   = models.CharField(max_length=45)
    worker_type = models.CharField(max_length=45)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'

class Photo(models.Model):
    description = models.TextField()
    url         = models.URLField(max_length=500)
    post        = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'photos'

class Tag(models.Model):
    point_x = models.DecimalField(decimal_places=3, max_digits=10)
    point_y = models.DecimalField(decimal_places=3, max_digits=10)
    photo   = models.ForeignKey(Photo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tags'