from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class UserSlot(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    slot_date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()

    class Meta:
        db_table = "UserSlot"
    def __str__(self):
    		return (self.user.username + "(" + str(self.user.id) +")")





