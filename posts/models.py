from django.db    import models

from core.models  import TimeStampModel
from users.models import User

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
