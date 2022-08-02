from django.db    import models

from core.models  import TimeStampModel

class User(TimeStampModel):
    kakao_id      = models.CharField(max_length=200, unique=True)
    email         = models.CharField(max_length=200, null=True)
    nickname      = models.CharField(max_length=50, null=True)
    profile_image = models.URLField(max_length=300, null=True)
    followers     = models.ManyToManyField('self',through='Follow')

    class Meta:
        db_table = 'users'

class Follow(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        db_table = 'follows'